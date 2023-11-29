import requests
import environ

from datetime import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

bot_token = env('TELEGRAM_BOT_TOKEN')
superuser_token = 'Bearer ' + env('SUPERUSER_TOKEN')


def signup(chat_id, username, first_name, last_name):
    try:
        url = 'http://51.250.77.9/api/v1/auth/'
        data = {'telegram_id': chat_id, 'username': username,
                'firstname': first_name, 'lastname': last_name}
        requests.post(url, data=data)
        text = get_template_text('greeting')
        msg = f'{first_name} {last_name}{text}'
        return msg
    except Exception:
        return 'Что-то пошло не так, попробуйте еще раз.'


def get_user_token(chat_id):
    url = f'http://51.250.77.9/api/v1/user/{chat_id}/'
    header = {'Authorization': superuser_token}
    response = requests.get(url, headers=header)
    user_data = response.json()
    return user_data


def get_template_text(temp_name):
    url = f'http://51.250.77.9/api/v1/template_text/{temp_name}/'
    header = {'Authorization': superuser_token}
    response = requests.get(url, headers=header)
    template_text = response.json()['text']
    return template_text


def update_usd_rate():
    try:
        url = 'http://51.250.77.9/api/v1/current_usd_rate/'
        header = {'Authorization': superuser_token}
        response = requests.get(url, headers=header)
        global current_usd_rate
        current_usd_rate = response.json()['usd_rate']
        return current_usd_rate
    except Exception:
        return

current_usd_rate = update_usd_rate()


def get_usd_rate(chat_id):
    try:
        user_token = 'Bearer ' + get_user_token(chat_id)['auth_token']
        header = {'Authorization': user_token}
        data = {'rate': current_usd_rate}
        url = 'http://51.250.77.9/api/v1/user_current_usd_rate/'
        requests.get(url, headers=header, data=data)
        text = get_template_text('current_rate')
        msg = f'{text}\n{current_usd_rate} {chr(8381)}'
        return msg
    except Exception:
        return 'Что-то пошло не так, попробуйте еще раз.'


def get_user_data(chat_id):
    try:
        user_token = 'Bearer ' + get_user_token(chat_id)['auth_token']
        header = {'Authorization': user_token}
        url = 'http://51.250.77.9/api/v1/me/'
        response = requests.get(url, headers=header)
        firstname = response.json()['firstname']
        lastname = response.json()['lastname']
        username = response.json()['username'] if response.json()['username'] else '-'
        chat_id = response.json()['telegram_id']
        notif = 'включены' if response.json()['notification'] else 'выключены'
        reg_date = dt.strptime(response.json()['reg_date'],
                            '%Y-%m-%dT%H:%M:%S.%f+03:00').strftime('%d.%m.%Y')
        msg = ('Данные о вашем аккаунте:\n'
            f'Имя: {firstname}\n'
            f'Фамилия: {lastname}\n'
            f'Username: {username}\n'
            f'Chat id: {chat_id}\n'
            f'Оповещения: {notif}\n'
            f'Дата регистрации: {reg_date}'
            )
        return msg
    except Exception:
        return 'Что-то пошло не так, попробуйте еще раз.'


def get_user_requests(chat_id):
    try:
        user_token = 'Bearer ' + get_user_token(chat_id)['auth_token']
        text = get_template_text('user_log')
        header = {'Authorization': user_token}
        url = 'http://51.250.77.9/api/v1/requests/'
        response = requests.get(url, headers=header)
        strptime = '%Y-%m-%dT%H:%M:%S.%f+03:00'
        date = lambda date: dt.strptime(date, strptime).strftime('%d.%m.%Y %H:%M')
        str_ = lambda str_: f"{date(str_['date'])}: {str_['rate']} {chr(8381)}"
        log = '\n'.join([str_(request) for request in response.json()])
        msg = f'{text}\n{log}'
        return msg
    except Exception:
        return 'Что-то пошло не так, попробуйте еще раз.'


def notification_subscription(chat_id):
    try:
        user_token = 'Bearer ' + get_user_token(chat_id)['auth_token']
        header = {'Authorization': user_token}
        url = 'http://51.250.77.9/api/v1/notification/'
        response = requests.patch(url, headers=header)
        if response.json()['notification']:
            msg = f'Вы успешно подписались на периодическое оповещение о курсе доллара.'
        else:
            msg = f'Вы успешно отписались от периодического оповещения о курсе доллара.'
        return msg
    except Exception:
        return 'Что-то пошло не так, попробуйте еще раз.'


def get_notification_list():
    notification_list = []
    try:
        url = 'http://51.250.77.9/api/v1/notification_list/'
        header = {'Authorization': superuser_token}
        response = requests.get(url, headers=header)
        notification_list = response.json()['notification_list']
        text = get_template_text('current_rate')
        msg = f'{text}\n{current_usd_rate} {chr(8381)}'
        return notification_list, msg
    except Exception:
        return notification_list, 'Что-то пошло не так, попробуйте еще раз.'
