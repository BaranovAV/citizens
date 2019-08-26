import pytest
import requests
import pymysql
from datetime import datetime
from settings import db
from model.imports import Import


def setup_module(module):
    print('start!')
    with pymysql.connect(**db) as cursor:
        print('connected to db!')
        cursor.execute('truncate table citizens')
        cursor.execute('truncate table imports')
        cursor.execute('truncate table relations')
    print('disconnected from db!')


def test_import_citizens(citizen_list):
    print(datetime.now())
    resp_post = requests.post(
        'http://0.0.0.0:8080/imports',
        headers={'Content-Type': 'application/json'},
        json={"citizens": citizen_list})
    print(datetime.now())
    assert resp_post.status_code == 201
    assert resp_post.json() == {'data': {'import_id': 1}}


def test_get_citizens(citizen_list):
    print(datetime.now())
    resp_get = requests.get(
        'http://0.0.0.0:8080/imports/1/citizens',
        headers={'Content-Type': 'application/json'})
    print(datetime.now())
    assert resp_get.status_code == 200
    assert resp_get.json() == {'data': citizen_list}


@pytest.mark.asyncio
@pytest.mark.parametrize('import_id,exist', [
    pytest.param(1, True),
    pytest.param(-1, False),
])
async def test_get_import(db_connection,import_id,exist):
    i = await Import.get_import(import_id, db_connection)
    assert (i is not None) == exist