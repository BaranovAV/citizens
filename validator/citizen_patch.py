from cerberus import Validator
from validator.base import _validate_date


def citizens_validator() -> 'Validator':
    return Validator({
        'citizens': {
            'type': 'list', 'minlength': 1, 'required': True, 'schema': {
                'type': 'dict', 'schema': {
                    'citizen_id': {'type': 'integer', 'required': True, 'min': 1, 'coerce': int},
                    'name': {'type': 'string', 'required': True, 'maxlength': 255},
                    'town': {'type': 'string', 'required': True, 'maxlength': 255},
                    'street': {'type': 'string', 'required': True, 'maxlength': 255},
                    'building': {'type': 'string', 'required': True, 'maxlength': 255},
                    'apartment': {'type': 'integer', 'required': True, 'min': 1, 'coerce': int},
                    'birth_date': {'type': 'string', 'required': True, 'validator': _validate_date('%d.%m.%Y')},
                    'gender': {'type': 'string', 'required': True, 'allowed': ['male', 'female']},
                    'relatives': {'type': 'list', 'minlength': 0, 'required': True, 'schema': {
                        'type': 'integer', 'min': 1, 'coerce': int}},
                }
            }
        }
    })
