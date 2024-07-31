import json
from urllib.parse import quote

import requests
from flask import Flask, request

from src.database.models import OneWinRegistration, OneWinDeposit
from src.handlers.user.kb import Keyboards
from src.handlers.user.messages import Messages
from config import Config


app = Flask(__name__)


def send_registration_success(user_id):
    text = Messages.get_registration_passed()
    reply_markup = Keyboards.get_check_deposit(user_id=user_id)
    url = (
        f'https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage?'
        f'chat_id={user_id}&text={quote(text)}'
        f'&reply_markup={quote(reply_markup.as_json())}&parse_mode=HTML'
    )
    requests.get(url)


def send_deposit_success(user_id):
    text = Messages.get_bot_activated()
    reply_markup = Keyboards.get_play()

    url = (
        f'https://api.telegram.org/bot{Config.BOT_TOKEN}/sendPhoto?'
        f'chat_id={user_id}&photo={Messages.get_bot_activated_photo()}'
        f'&caption={quote(text)}'
        f'&reply_markup={quote(reply_markup.as_json())}&parse_mode=HTML'
    )
    requests.get(url)


def send_notification(text: str):
    for admin_id in Config.ADMIN_IDS:
        requests.get(
            f'https://api.telegram.org/bot{Config.POSTBACK_BOT_TOKEN}/'
            f'sendMessage?chat_id={admin_id}&text={text}'
        )


@app.route('/', methods=['GET'])
def index():
    return "I'm alive!"


@app.route("/registration", methods=['GET'])
def registration():
    one_win_id = request.args.get('user_id')
    sub1 = request.args.get('sub1')

    text = f"Регистрация: {one_win_id} sub1:{sub1}"
    send_notification(text=text)

    OneWinRegistration.get_or_create(one_win_id=one_win_id, sub1=sub1)
    send_registration_success(user_id=sub1)

    return 'OK: 200'


@app.route('/deposit')
def deposit():
    one_win_id = request.args.get('user_id')
    amount = request.args.get('amount')
    sub1 = request.args.get('sub1')

    text = f'{one_win_id} : депозит : {amount}  sub1:{sub1}'
    send_notification(text=text)

    OneWinDeposit.get_or_create(sub1=sub1, one_win_id=one_win_id, amount=amount)
    send_deposit_success(user_id=sub1)

    return 'OK: 200'


def run_app():
    while True:
        try:
            app.run(host="0.0.0.0", port=Config.POSTBACK_PORT)
        except Exception as ex:
            print(ex)

