#!/usr/bin/env python3

import requests
import string
import time

password = ''
last_password = 'placeholder'
position = 15

while password != last_password:
    last_password = password

    data = {'user': 'f' * (position - len(password))}
    #r = requests.post('http://crypto1.crikey.ctf:5000/login', data = data)
    r = requests.post('http://localhost:5000/login', data = data)
    if r.status_code != 200:
        print('status_code:', r.status_code)
        exit(1)
    reference = r.cookies['user_colon_pass'][:32]

    print(string.ascii_letters + string.digits + ':')

    for x in (string.ascii_letters + string.digits + ':'):
        data = {'user': 'f' * (position - len(password)) + password + x}
        #r = requests.post('http://crypto1.crikey.ctf:5000/login', data = data)
        r = requests.post('http://localhost:5000/login', data = data)
        if r.status_code != 200:
            print('status_code:', r.status_code)
            exit(1)
        if r.cookies['user_colon_pass'][:32] == reference:
            print(x, end='', flush=True)
            password += x
            break
        else:
            print('.', end='', flush=True)
        time.sleep(0.1)

    print('\n' + password)
    time.sleep(0.1)
