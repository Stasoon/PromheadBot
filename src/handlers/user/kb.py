from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData

from config import Config


class Keyboards:
    locale_callback_data = CallbackData('locale', 'language_code')
    deposit_check_callback = CallbackData('check_dep', 'one_win_id')
    game_callback = CallbackData('game', 'name')

    @staticmethod
    def get_choose_game() -> InlineKeyboardMarkup:
        aviator = InlineKeyboardButton(text='✈️ AVIATOR ✈️', callback_data=Keyboards.game_callback.new(name='aviator'))
        mines = InlineKeyboardButton(text='⭐️ MINES ⭐️', callback_data=Keyboards.game_callback.new(name='mines'))
        bombucks = InlineKeyboardButton(text='💲 BOMBUCKS 💲', callback_data=Keyboards.game_callback.new(name='bombucks'))
        return InlineKeyboardMarkup(row_width=2).add(aviator).row(mines, bombucks)

    @staticmethod
    def get_check_registration() -> InlineKeyboardMarkup:
        check_registration = InlineKeyboardButton(text='CHECK ID ✅', callback_data='check_registration')
        return InlineKeyboardMarkup(row_width=1).add(check_registration)

    @staticmethod
    def get_check_deposit(user_id) -> InlineKeyboardMarkup:
        deposit = InlineKeyboardButton(text='TOP UP YOUR BALANCE', url=Config.get_registration_link(user_id=user_id))
        check = InlineKeyboardButton(text='TOPPED UP? PRESS HERE ✅', callback_data='check_deposit')
        return InlineKeyboardMarkup(row_width=1).add(deposit, check)

    @staticmethod
    def get_play(game_name: str = 'mines') -> InlineKeyboardMarkup:
        game_url = f'https://stasmoons.github.io/PromheadSite/{game_name}/index.html'
        play = InlineKeyboardButton(text='👉 SIGNAL ⭐️', web_app=WebAppInfo(url=game_url))
        menu = InlineKeyboardButton(text='🔙 MENU 🔙', callback_data='menu')
        return InlineKeyboardMarkup(row_width=1).add(play, menu)

    @staticmethod
    def get_bombucks_signal() -> InlineKeyboardMarkup:
        play = InlineKeyboardButton(text='👉 SIGNAL ⭐️', callback_data='bombucks_signal')
        menu = InlineKeyboardButton(text='🔙 MENU 🔙', callback_data='menu')
        return InlineKeyboardMarkup(row_width=1).add(play, menu)

