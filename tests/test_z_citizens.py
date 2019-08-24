import pytest
import requests
from datetime import datetime


@pytest.mark.parametrize('url,data,code', [
    pytest.param(
        'imports/1/citizen/3334',
        {},
        400,
        id='no data was sent (400)'
    ),
    pytest.param(
        'imports/1/citizen/3334',
        {'name': '', 'town': ''},
        400,
        id='bad data was sent (400)'
    ),
    pytest.param(
        'imports/1/citizen/13334',
        {'relatives': []},
        404,
        id='citizen not exists (404)'
    ),
    pytest.param(
        'imports/1/citizen/3334',
        {'relatives': []},
        200,
        id='ok (removed all relations)'
    ),
    pytest.param(
        'imports/1/citizen/3334',
        {'relatives': [16, 1103, 4225, 5244, 9811]},
        200,
        id='ok (restored all relations)'
    ),
])
def test_patch_citizen(url, data, code):
    print(datetime.now())
    print(requests.get(f'http://0.0.0.0:8080/{url}',
                       headers={'Content-Type': 'application/json'}).json())
    resp_patch = requests.patch(
        f'http://0.0.0.0:8080/{url}',
        headers={'Content-Type': 'application/json'},
        json=data)
    print(requests.get(f'http://0.0.0.0:8080/{url}',
                       headers={'Content-Type': 'application/json'}).json())
    print(datetime.now())
    assert resp_patch.status_code == code
