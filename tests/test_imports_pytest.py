import json
import pytest
import requests
import pymysql
from datetime import datetime
from settings import db
from validator.import_citizens import validate_by_chunks, validate_relations


def setup_module(module):
    print('start!')
    with pymysql.connect(**db) as cursor:
        print('connected to db!')
        cursor.execute('truncate table citizens')
        cursor.execute('truncate table imports')
        cursor.execute('truncate table relations')
    print('disconnected from db!')


def test_good_import():
    # citizens = [
    #     {
    #         "citizen_id": i,
    #         "town": "Москва",
    #         "street": "Льва Толстого",
    #         "building": "16к7стр5",
    #         "apartment": 7,
    #         "name": f"Иванов Иван Иванович {i}",
    #         "birth_date": "16.12.1986",
    #         "gender": "male",
    #         "relatives": []
    #     } for i in range(1, 10001)
    # ]
    # from random import randint
    # for k in range(1, 12001):
    #     while True:
    #         i = randint(1, 5 * k) % 10000 + 1
    #         j = randint(i, 15 * k) % 10000 + 1
    #         if i != j:
    #             break
    #     citizens[i - 1]['relatives'].append(j)
    #     citizens[i - 1]['relatives'].sort()
    #     citizens[j - 1]['relatives'].append(i)
    #     citizens[j - 1]['relatives'].sort()
    #
    # with open('test-data.txt', 'w') as f:
    #     f.write(json.dumps(citizens))
    #
    with open('test-data.txt', 'r') as f:
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


@pytest.mark.asyncio
async def test_validator():
    with open('test-data.txt', 'r') as f:
        citizens = {'citizens': json.loads(f.read())}

    from validator.import_citizens import citizens_validator
    v = citizens_validator()
    data, _errors = await validate_by_chunks(v, citizens['citizens'], 'citizens')
    assert _errors == []


@pytest.mark.parametrize("lst,out", [
    pytest.param(
        [{'citizen_id': 1, 'relations': [2]}, {'citizen_id': 2, 'relations': [1]}, {'citizen_id': 3, 'relations': []}],
        [],
        id='GOOD'
    ),
    pytest.param(
        [{'citizen_id': 2, 'relations': [1]}],
        ['2 has single linked relation with 1'],
        id='BAD'
    ),
    pytest.param(
        [{'citizen_id': 1, 'relations': [2]}, {'citizen_id': 2, 'relations': []}],
        ['1 has single linked relation with 2'],
        id='BAD'
    ),
    pytest.param(
        [{'citizen_id': 1, 'relations': [2]}, {'citizen_id': 2, 'relations': [1, 1]}],
        ['duplicated ids found in relations for 2'],
        id='BAD'
    ),
])
def test_validate(lst, out):
    assert validate_relations(lst) == out
