import variable as vb
import requests
import re
import Weather as wt

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

#Chat ID
def get_chat_id():
    return get_update()['result'][-1]['message']['chat']['id']
    pass

#Last message
def get_last_message():
    return get_update()['result'][-1]['message']['text']
    pass


def parse_text_money():
    pattern=r'/\w+'
    return re.search(pattern, get_last_message()).group()

#Update message
def get_updates(message):
    res = requests.get(url_money.format(message))
    return res.json()
    pass

#Get rates
def get_money(message):
    date=get_updates(message)['Date']
    name=get_updates(message)['Cur_Name']
    rate=get_updates(message)['Cur_OfficialRate']
    return 'За {}, курс {}, за 1 {}'.format(date, rate, name)
    pass

#api_key='c200df268902d5a73de7e6b6563f745e'
api_weather='http://api.openweathermap.org/data/2.5/find?q{}&type=like&lang=ru&APPID=c200df268902d5a73de7e6b6563f745e'

#Update weather
def get_weather_update(city):
    res=requests.get(api_weather.format(city))
    return res.json()
    pass

#Get weather
def get_weather_message(m):
    name=get_weather_update(m)['list'][0]['name']
    conditions=get_weather_update(m)['list'][0]['weather'][0]['description']
    temp=get_weather_update(m)['list'][0]['main']['temp']
    temp_min=get_weather_update(m)['list'][0]['main']['temp_min']
    temp_max=get_weather_update(m)['list'][0]['main']['temp_max']
    return 'Город: {}, температура: {} , {}'.format(name, temp ,conditions)


#Help
def get_message():
    if '/' in get_last_message():
        return get_money(parse_text_money())
    elif '=' in get_last_message():
        return get_weather_message(get_last_message())
    else:
        return 'Для вывода валюты введите /usd\n' \
               'Для вывода погоды введите =Brest,BY'


#Send Message
def send_message():
    chat_id=get_chat_id()
    text=get_message()
    params = {'chat_id': chat_id, 'text': text}
    requests.post(tel_api_url.format(token) + send, params)



def main():
    send_message()


if __name__ == '__main__':
    main()