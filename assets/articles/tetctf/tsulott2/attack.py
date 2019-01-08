#!/usr/bin/env python2

import codecs
import requests
import re

ss = requests.Session()

def flip(enc):
    enc = codecs.decode(enc, "hex_codec")
    iv, ct = (enc[:16], enc[16:])
    iv = iv[:15] + chr(ord(iv[15]) ^ ord('0') ^ ord('_'))
    return codecs.encode(iv + ct, "hex_codec")

def lott(ticket):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'ticket': ticket
    }

    return ss.post('http://149.28.144.129/lott', headers=headers, data=data)

def ticket(number, bet):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'number': str(number),
        'bet': str(bet)
    }

    return ss.post('http://149.28.144.129/ticket', headers=headers, data=data)

def market(buy):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'buy': buy
    }

    return ss.post('http://149.28.144.129/market', headers=headers, data=data)

def home(take):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'take': take
    }

    return ss.post('http://149.28.144.129/', headers=headers, data=data)

def reset():
    return ss.get('http://149.28.144.129/reset')

ok = False

while not ok:
    reset()
    lines = ticket(1, 100000000000000).text.split("\n")
    t = ""

    for line in lines:
        if "Here your ticket:" in line:
            t = line.strip().replace("Here your ticket: ", "")
            break

    lines = lott(flip(t)).text.split("\n")

    for line in lines:
        if "Your guess: 1" in line:
            tokens = line.strip().split()
        
            if int(tokens[1]) == 1:
                ok = True

            break

market("flag")
print re.search("TetCTF{(.+?)}", home("flag").text).group(0)
