from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData

from config import Config


class Keyboards:
    locale_callback_data = CallbackData('locale', 'language_code')
    deposit_check_callback = CallbackData('check_dep', 'one_win_id')
    game_callback = CallbackData('game', 'name')

    @staticmethod
    def get_choose_game() -> InlineKeyboardMarkup:
        mines = InlineKeyboardButton(text='⭐️ MINES ⭐️', callback_data=Keyboards.game_callback.new(name='mines'))
        royal_mines = InlineKeyboardButton(text='💣 ROYAL MINES 💣', callback_data=Keyboards.game_callback.new(name='royal_mines'))
        bombucks = InlineKeyboardButton(text='💲 BOMBUCKS 💲', callback_data=Keyboards.game_callback.new(name='bombucks'))

        brawl_pirates = InlineKeyboardButton(text='☠️ BRAWL PIRATES ☠️', callback_data=Keyboards.game_callback.new(name='brawl_pirates'))
        football_x = InlineKeyboardButton(text='⚽️ FOOTBALL X ⚽️', callback_data=Keyboards.game_callback.new(name='football_x'))
        aviator = InlineKeyboardButton(text='✈️ AVIATOR ✈️', callback_data=Keyboards.game_callback.new(name='aviator'))

        return InlineKeyboardMarkup(row_width=2).add(mines, royal_mines, bombucks,   brawl_pirates, football_x, aviator)

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
        if game_name in ('aviator', 'mines'):
            game_url = f'https://stasmoons.github.io/PromheadSite/{game_name}/index.html'
            play = InlineKeyboardButton(text='👉 SIGNAL ⭐️', web_app=WebAppInfo(url=game_url))
        else:
            play = InlineKeyboardButton(text='👉 SIGNAL ⭐️', callback_data='signal')

        menu = InlineKeyboardButton(text='🔙 MENU 🔙', callback_data='menu')
        return InlineKeyboardMarkup(row_width=1).add(play, menu)

