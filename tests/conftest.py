import json
import os
import aiomysql
import pytest
from settings import db


@pytest.fixture(scope='module')
def citizen_list():
    with open(os.path.abspath('tests') + '/test-data.txt', 'r') as f:
        yield json.loads(f.read())


@pytest.fixture(scope='function')
async def db_connection():
    async with aiomysql.connect(
            host=db['host'],
            db=db['database'],
            user=db['user'],
            password=db['password'],
            autocommit=db['autocommit'],
            charset=db['charset']) as conn:
        yield conn