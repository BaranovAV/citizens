import json
import os
import requests
import pymysql
from datetime import datetime
from settings import db


def setup_module(module):
    print('start!')
    with pymysql.connect(**db) as cursor:
        print('connected to db!')
        cursor.execute('truncate table citizens')
        cursor.execute('truncate table imports')
        cursor.execute('truncate table relations')
    print('disconnected from db!')


def test_import_citizens():
    with open(os.path.abspath('tests') + '/test-data.txt', 'r') as f:
        citizens = json.loads(f.read())

    print(datetime.now())
    resp_post = requests.post(
        'http://0.0.0.0:8080/imports',
        headers={'Content-Type': 'application/json'},
        json={"citizens": citizens})
    print(datetime.now())
    assert resp_post.status_code == 201
    assert resp_post.json() == {'data': {'import_id': 1}}

    resp_get = requests.get(
        'http://0.0.0.0:8080/imports/1/citizens',
        headers={'Content-Type': 'application/json'})
    print(datetime.now())
    assert resp_get.status_code == 200
    assert resp_get.json() == {'data': citizens}
