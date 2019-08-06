import variable as vb
import requests
import re

#bot
upd = vb.methods['updates']
send = vb.methods['send']
tel_api_url=vb.tel_api_url
token=vb.bot_token

#money
url_money='http://www.nbrb.by/api/exrates/rates{}?parammode=2'

def get_update():
    res=requests.get(tel_api_url.format(token)+upd)
    return res.json()
    pass


def get_chat_id():
    return get_update()['result'][-1]['message']['chat']['id']
    pass


def get_last_message():
    return get_update()['result'][-1]['message']['text']
    pass


def parse_text():
    pattern=r'/\w+'
    return re.search(pattern, get_last_message()).group()


def get_update_money():
    res = requests.get(url_money.format(parse_text()))
    return res.json()
    pass


def get_money():
    date=get_update_money()['Date']
    name=get_update_money()['Cur_Name']
    rate=get_update_money()['Cur_OfficialRate']
    return 'За {}, курс {}, за 1 {}'.format(date, rate, name)
    pass


def send_message():
    chat_id=get_chat_id()
    text=get_money()
    params = {'chat_id': chat_id, 'text': text}
    requests.post(tel_api_url.format(token) + send, params)



def main():
    send_message()


if __name__ == '__main__':
    main()