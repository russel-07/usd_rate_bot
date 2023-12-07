import os
import requests

from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv('../../.env')


bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
superuser_tg_id = os.getenv('SUPERUSER_TG_ID')
superuser_password = os.getenv('SUPERUSER_PASSWORD')
api_url = os.getenv('API_URL')


def signup(chat_id, firstname, lastname, username):
    url = api_url + 'user/'
    token = get_superuser_token()
    data = {'telegram_id': chat_id, 'firstname': firstname,
            'lastname': lastname, 'username': username}
    response = requests.post(url, headers=token, data=data)
    if response.status_code == 201:
        text = get_template_text('greeting', token)
        msg = text.format(**data)
    else:
        msg = 'Вы уже зарегистрированы. Проверка!'
    return msg


def get_user_data(chat_id):
    url = api_url + f'user/{chat_id}'
    token = get_superuser_token()
    response = requests.get(url, headers=token)
    if response.status_code == 200:
        data = response.json()
        dt_frmt = '%Y-%m-%dT%H:%M:%S.%f+03:00'
        data['notification'] = 'включены проверка' if data['notification'] \
            else 'выключены проверка'
        data['reg_date'] = dt.strptime(data['reg_date'], dt_frmt) \
            .strftime('%d.%m.%Y')
        text = get_template_text('user_data', token)
        msg = text.format(**data)
        return msg


def change_user_notification_status(chat_id):
    url = api_url + f'user/{chat_id}/'
    token = get_superuser_token()
    response = requests.get(url, headers=token)
    if response.status_code == 200:
        user_notification_status = not response.json()['notification']
        data = {'notification': user_notification_status}
        response = requests.patch(url, headers=token, data=data)
        if response.status_code == 200:
            if user_notification_status:
                msg = 'Вы успешно подписались на периодическое' \
                      ' оповещение о курсе доллара. Проверка!'
            else:
                msg = 'Вы успешно отписались от периодического' \
                      ' оповещения о курсе доллара.'
            return msg


def get_user_requests(chat_id):
    url = api_url + f'user/{chat_id}/requests/'
    token = get_superuser_token()
    response = requests.get(url, headers=token)
    if response.status_code == 200:
        data = response.json()
        if data:
            text = [get_template_text('user_requests', token)]
            strptime_ = '%Y-%m-%dT%H:%M:%S.%f+03:00'
            strftime_ = '%d.%m.%Y %H:%M'
            for request in data:
                date = dt.strptime(request['date'], strptime_) \
                       .strftime(strftime_)
                rate = f"{request['rate']} {chr(8381)}"
                text.append(f'{date}: {rate}')
            msg = '\n'.join(text)
        else:
            msg = 'У вас пока нет запросов.'
        return msg


def get_usd_rate(chat_id):
    url = api_url + f'user/{chat_id}/requests/'
    token = get_superuser_token()
    data = {'rate': current_usd_rate}
    response = requests.post(url, headers=token, data=data)
    if response.status_code == 201:
        text = get_template_text('rate', token)
        msg = text.format(rate=current_usd_rate, rub_sign=chr(8381))
        url = api_url + f'user/{chat_id}/'
        response = requests.get(url, headers=token)
        if response.status_code == 200:
            notification_status = response.json()['notification']
            return msg, notification_status


def get_superuser_token():
    url = api_url + 'token/'
    data = {'telegram_id': superuser_tg_id, 'password': superuser_password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token = {'Authorization': f"Bearer {response.json()['access']}"}
        return token


def update_usd_rate():
    global current_usd_rate
    url = api_url + 'rate/'
    token = get_superuser_token()
    response = requests.get(url, headers=token)
    if response.status_code == 200:
        current_usd_rate = response.json()['usd_rate']
        return current_usd_rate


def get_notified_list():
    url = api_url + 'notified_list/'
    token = get_superuser_token()
    response = requests.get(url, headers=token)
    if response.status_code == 200:
        notified_list = response.json()['notified_list']
        text = get_template_text('rate', token)
        msg = text.format(rate=current_usd_rate, rub_sign=chr(8381))
        return notified_list, msg


def get_template_text(temp_name, token):
    url = api_url + f'template_text/{temp_name}/'
    response = requests.get(url, headers=token)
    if response.status_code == 200:
        template_text = response.json()['text']
        return template_text


current_usd_rate = update_usd_rate()
