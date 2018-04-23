#!/usr/bin/env python3

# DEPS: apt-get install python3-crypto python3-flask

import binascii
from Crypto.Cipher import AES
from flask import Flask, make_response, request

flag = 'flag{stop_repeating_yourself}'
server_header = 'ACrikey' 
secret = '84z2rEweK922'

def pad(text):
    mod = len(text) % AES.block_size
    if mod != 0:
        padding = AES.block_size - mod
        text += bytes([padding]) * padding
    return text

def encode(text):
    cipher = AES.new(b'\x15\x50\xb2\xef\x93\xd2\x5f\xcd\xb9\x8c\x57\x32\xcc\x57\x34\xa0', AES.MODE_ECB, b'\x00' * 16)
    ct = cipher.encrypt(pad(bytes(text, encoding='utf-8')))
    return binascii.hexlify(ct)

def main():
    app = Flask(__name__)
    @app.route('/')
    def index():
        result = '''<!DOCTYPE html>
<html>
  <head>
    <title>CMS</title>
  </head>
  <body>
    <h1>CMS</h1>
    <h2>Create a user here:</h2>
    <p>Accounts will all be created with the same initial default password.</p>
    <form action="/login" method="post">
      <p>User:<br><input maxlength=8 name="user" type="text"></p>
      <p><input type="submit" value="Create"></p>
    </form>
    <h2>Log in here with an existing user:</h2>
    <p>The administrative user is named admin.</p>
    <p>Passwords can be up to 16 alphanumeric characters.</p>
    <form action="/login" method="post">
      <p>User:<br><input maxlength=8 name="user" type="text"></p>
      <p>Pass:<br><input maxlength=16 name="pass" type="password"></p>
      <p><input type="submit" value="Login"></p>
    </form>
  </body>
</html>
'''
        resp = make_response(result)
        resp.headers['Server'] = server_header
        return resp, 200

    @app.route('/login', methods=['POST'])
    def login():
        form_user = request.form.get('user', None)
        if form_user:
            form_user = ''.join(x for x in form_user if (x.isalnum() or x == ':'))
        form_pass = request.form.get('pass', None)
        if form_pass:
            form_pass = ''.join(x for x in form_pass if x.isalnum())
        result = '''<!DOCTYPE html>
<html>
  <head>
    <title>CMS</title>
  </head>
  <body>
'''
        if form_user and form_pass:
            if encode(form_pass) == encode(secret):
                if form_user.lower() == 'admin':
                    result += '    <p>Nice work! The flag is ' + flag + '.</p>\n'
                else:
                    result += '    <p>Sorry, only admin mode is implemented.</p>\n'
            else:
                result += '    <p>Sorry, your password is incorrect.</p>\n'
            result += '  </body>\n</html>\n'
            resp = make_response(result)
            resp.headers['Server'] = server_header
            return resp, 200

        elif form_user and not form_pass:
            if form_user.lower() == 'admin':
                result += '    <p>Can not create the admin account.</p>\n'
                result += '  </body>\n</html>\n'
                resp = make_response(result)
                resp.headers['Server'] = server_header
                return resp, 200
            else:
                result += '    <p>Account created.</p>\n'
                result += '  </body>\n</html>\n'
                resp = make_response(result)
                resp.headers['Server'] = server_header
                resp.set_cookie('user_colon_pass', encode(form_user + ':' + secret))
                return resp, 200

        else:
            result += '    <p>User is required.</p>\n'
            result += '  </body>\n</html>\n'
            resp = make_response(result)
            resp.headers['Server'] = server_header
            return resp, 200

    # start the web server
    app.run(host="0.0.0.0", port=5000, threaded=True)

if __name__ == "__main__":
    main()
