import pytest
from validator.import_citizens import validate_by_chunks, validate_relations


@pytest.mark.asyncio
async def test_validate_by_chunks(citizen_list):
    from validator.import_citizens import citizens_validator
    v = citizens_validator()
    data, _errors = await validate_by_chunks(v, citizen_list, 'citizens')
    assert _errors == []


@pytest.mark.parametrize("lst,out", [
    pytest.param(
        [{'citizen_id': 1, 'relatives': [2]}, {'citizen_id': 2, 'relatives': [1]}, {'citizen_id': 3, 'relatives': []}],
        [],
        id='good relations'
    ),
    pytest.param(
        [{'citizen_id': 2, 'relatives': [1]}],
        ['2 has single linked relation with 1'],
        id='related to unexisting user'
    ),
    pytest.param(
        [{'citizen_id': 1, 'relatives': [2]}, {'citizen_id': 2, 'relatives': []}],
        ['1 has single linked relation with 2'],
        id='single relation'
    ),
    pytest.param(
        [{'citizen_id': 1, 'relatives': [2]}, {'citizen_id': 2, 'relatives': [1, 1]}],
        ['duplicated ids found in relatives for 2'],
        id='duplicated relation'
    ),
])
def test_validate_relations(lst, out):
    assert validate_relations(lst) == out
