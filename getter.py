import requests
import time


host = 'http://127.0.0.1:5000'
url = '/get_messages'
after = 0

while True:
    response = requests.get(host+url)
    messages = response.json()['messages']
    for messag in messages:
        if messag['timestamp'] > after:
            print(messag['username'], 'говорит')
            print('   ', messag['text'])
            print()
    after = messag['timestamp']
    time.sleep(5)
