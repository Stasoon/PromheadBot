import os
import random

from aiogram.types import InputFile
from aiogram.utils.markdown import quote_html

from config import Config


class Messages:
    #  Статья с фото: https://telegra.ph/photos-promhead-bot-06-24

    @staticmethod
    def get_welcome(user_name: str = 'незнакомец') -> str:
        return (
            "Choose a game ⤵️"
            # "✅ <b>New bot developed this year is already available for you</b> 🚀 \n\n"
            #
            # "1️⃣ The bot will allow you to consistently earn every day on the <b>MINES game</b> \n\n"
            #
            # "2️⃣ Real earnings from <b>$50-100</b> every day!💰 \n\n"
            #
            # "3️⃣ The bot gives signals with a <b>90%</b> success rate using artificial intelligence! \n\n"
            #
            # "🎁 Now PRESS FURTHER ↘️"
        )

    @staticmethod
    def get_welcome_photo() -> str:
        return 'https://telegra.ph/file/baadc59be30da2f5d3057.png'

    @staticmethod
    def get_registration(user_id: int, game_name: str):
        match game_name:
            case 'aviator': game_name_text = 'AVIATOR ✈️'
            case 'bombucks': game_name_text = 'BOMBUCKS 💲'
            case _: game_name_text = 'MINES 💣'

        return (
            f'Welcome to <b>{game_name_text}</b> \n\n'

            'Activate the bot ☑️ \n'
            '1. Create a new account using this link ⤵️ \n'
            f'➡️ {Config.get_registration_link(user_id=user_id)} \n\n'
            
            '2. After registration, click \n'
            'the <b>CHECK ID</b> \n\n'

            '🎰 With the help of a bot you can consistently earn <b>$50-200</b> daily!'
        )

    @staticmethod
    def get_registration_photo(game_name: str) -> str:
        match game_name:
            case 'aviator': return 'https://telegra.ph/file/97c212e0b4e0c9b6d3002.png'
            case 'bombucks': return 'https://telegra.ph/file/26a204c8437929da6c381.png'
            case _: return 'https://telegra.ph/file/5391d4a3bbf828869cc6d.png'

    @staticmethod
    def get_registration_passed():
        return (
            '<b>REGISTRATION COMPLETED</b> ✅ \n\n'
            
            'Now top up your balance by <b>$5-10</b> (use any currency) \n\n'

            'This amount is needed to work with the bot. '
            'After replenishing the balance, the <b>BOT</b> is activated❗️ \n\n'

            '<b>You can earn from $50-$100 every day</b> 💰'
        )

    @staticmethod
    def get_registration_not_passed(user_id: int):
        return (
            f'Account ID is not correct ❌ \n\n' 
            f'Create a new one using this link: {Config.get_registration_link(user_id=user_id)}'
        )

    @staticmethod
    def get_deposit_not_found():
        return '❗️Your deposit was not found, please try again.'

    @staticmethod
    def get_bot_activated():
        private_channel_link = 'https://t.me/+H4zf0sONYL0wNmUy'
        return (
            '✅ <b>BOT ACTIVATED</b>⭐️ \n\n'

            'Click the <b>SIGNALS</b> button and start earning money! \n\n'

            'A private channel is available to you, stay tuned for updates to the bot! \n'
            f'➡️ {private_channel_link} \n<b>(subscribe)</b>'
        )

    @staticmethod
    def get_bot_activated_photo():
        return 'https://telegra.ph/file/ff0ebfda2488a16a1f304.png'

    @staticmethod
    def get_bombucks_signal_photo():
        images_dir_path = os.path.join('resources', 'bombucks')
        files = [
            filename for filename in os.listdir(images_dir_path)
            if filename.endswith('.png') or filename.endswith('.jpg')
        ]

        random_filename = random.choice(files)
        image_path = os.path.join(images_dir_path, random_filename)
        return InputFile(image_path)
