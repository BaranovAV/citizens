from cerberus import Validator
from validator.base import _validate_date


def citizen_validator() -> 'Validator':
    return Validator({
        'name': {'type': 'string', 'minlength': 1, 'maxlength': 255},
        'town': {'type': 'string', 'minlength': 1, 'maxlength': 255},
        'street': {'type': 'string', 'minlength': 1, 'maxlength': 255},
        'building': {'type': 'string', 'minlength': 1, 'maxlength': 255},
        'apartment': {'type': 'integer', 'min': 1, 'coerce': int},
        'birth_date': {'type': 'string', 'check_with': _validate_date('%d.%m.%Y')},
        'gender': {'type': 'string', 'allowed': ['male', 'female']},
        'relatives': {'type': 'list', 'minlength': 0, 'schema': {
            'type': 'integer', 'min': 1, 'coerce': int
        }},
    })
