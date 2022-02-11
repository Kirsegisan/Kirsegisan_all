import requests
import time


host = 'http://127.0.0.1:5000'
url = '/send_messages'
login_url = '/login_messages'


username = input('Введи своё имя: ')
password = input('введите пороль: ')
response = requests.post(
    host+url,
    json={'username': username, 'password': password})

while not response.json()['ok']:
    print('неверный логин или пороль!')
    print('')
    username = input('Введи своё имя: ')
    password = input('введите пороль: ')
    respons = requests.post(
        host+url,
        json={'username': username, 'password': password})

print('Welcome!')

while True:
    text = input("Введи текст сообщения:")

    requests.post(
        host+url,
        json={'username': username, 'text': text}
    )