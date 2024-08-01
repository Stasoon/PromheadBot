from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatMemberStatus
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import BadRequest, RetryAfter
from peewee import fn

from src.database import users
from src.database.models import OneWinRegistration, OneWinDeposit
from src.utils import send_typing_action
from .messages import Messages
from .kb import Keyboards
from src.database.models import ChannelJoinRequest


# region Utils

async def is_user_subscribed(bot, user_id: int, channel_id: int) -> bool:
    """ Проверить, подписан ли пользователь на канал / подавал ли заявку """
    if ChannelJoinRequest.get_or_none(user_id=user_id, channel_id=channel_id):
        return True

    try: channel_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    except (BadRequest, RetryAfter) as e:
        print(e)
        return True
    except Exception:
        return False

    if channel_member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return False
    return True


# endregion


# region Handlers

async def __handle_start_command(message: Message, state: FSMContext) -> None:
    await state.finish()
    await send_typing_action(message)

    users.create_or_update_user(
        telegram_id=message.from_id,
        name=message.from_user.username or message.from_user.full_name,
        reflink=message.get_full_command()[1]
    )

    await message.answer_photo(
        photo=Messages.get_welcome_photo(),
        caption=Messages.get_welcome(message.from_user.first_name),
        reply_markup=Keyboards.get_choose_game()
    )


async def handle_game(callback: CallbackQuery, callback_data: Keyboards.game_callback):
    await callback.answer()

    game_name = callback_data.get('name')
    user = users.get_user_or_none(telegram_id=callback.from_user.id)
    user.game = game_name
    user.save()

    user_deposit = OneWinDeposit.get_or_none(sub1=callback.from_user.id)
    if user_deposit:
        markup = Keyboards.get_play(game_name=user.game)
        await callback.message.answer(
            text='Click the <b>SIGNALS</b> button and start earning money!',
            reply_markup=markup
        )
        return

    await callback.message.answer_photo(
        photo=Messages.get_registration_photo(game_name=game_name),
        caption=Messages.get_registration(user_id=callback.from_user.id, game_name=game_name),
        reply_markup=Keyboards.get_check_registration(),
        # disable_web_page_preview=True
    )


async def handle_check_registration(callback: CallbackQuery):
    await callback.answer()
    one_win_registration = OneWinRegistration.get_or_none(OneWinRegistration.sub1 == callback.from_user.id)

    if not one_win_registration:
        text = Messages.get_registration_not_passed(user_id=callback.from_user.id)
        markup = Keyboards.get_check_registration()
        await callback.message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
    else:
        text = Messages.get_registration_passed()
        markup = Keyboards.get_check_deposit(user_id=callback.from_user.id)
        await callback.message.answer(text=text, reply_markup=markup)

        user = users.get_user_or_none(telegram_id=callback.from_user.id)
        user.onewin_id = one_win_registration.one_win_id
        user.save()


async def handle_check_deposit(callback: CallbackQuery):
    user = users.get_user_or_none(telegram_id=callback.from_user.id)
    user_deposits_sum = (
        OneWinDeposit
        .select(fn.SUM(OneWinDeposit.amount))
        .where(OneWinDeposit.one_win_id == user.onewin_id)
        .scalar()
    )

    if not user_deposits_sum:
        user_deposits_sum = 0.0

    if user_deposits_sum == 0:
        await callback.answer(text=Messages.get_deposit_not_found(), show_alert=True)
    else:
        await callback.answer()
        markup = Keyboards.get_play(game_name=user.game)
        await callback.message.answer(text=Messages.get_bot_activated(), reply_markup=markup)


async def handle_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(
        photo=Messages.get_welcome_photo(),
        caption=Messages.get_welcome(callback.from_user.first_name),
        reply_markup=Keyboards.get_choose_game()
    )


async def handle_signal(callback: CallbackQuery):
    await callback.answer()

    user = users.get_user_or_none(telegram_id=callback.from_user.id)
    signal_photo = Messages.get_signal_photo(game_name=user.game)
    markup = Keyboards.get_play(game_name=user.game)
    await callback.message.answer_photo(photo=signal_photo, reply_markup=markup)


# endregion


def register_user_handlers(dp: Dispatcher) -> None:
    # обработка команды /start
    dp.register_message_handler(__handle_start_command, commands=['start'], state='*')
    dp.register_callback_query_handler(handle_game, Keyboards.game_callback.filter())

    # смена игры
    dp.register_callback_query_handler(handle_menu, text='menu')

    # регистрация
    dp.register_callback_query_handler(handle_check_registration, text='check_registration')

    dp.register_callback_query_handler(handle_check_deposit, text='check_deposit')

    #
    dp.register_callback_query_handler(handle_signal, text='signal')

