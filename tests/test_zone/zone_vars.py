import json
import logging
import random
import string

from mdssdk.switch import Switch

logging.basicConfig(filename='test_zone.log', filemode='w', level=logging.INFO,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

def get_random_id(start=2, end=400):
    return random.randint(start, end)

def get_random_pwwn():
    choicelist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    entry = ""
    for i in range(16):
        e = random.choice(choicelist)
        entry = entry + e
        if i % 2 == 1:
            entry = entry + ":"
    return entry.rstrip(":")


def get_random_string(n=5):
    return ''.join(random.choices(string.ascii_letters, k=n))