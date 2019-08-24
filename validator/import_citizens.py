from cerberus import Validator
from validator.base import _validate_date, _get_error_list


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
                    'birth_date': {'type': 'string', 'required': True, 'check_with': _validate_date('%d.%m.%Y')},
                    'gender': {'type': 'string', 'required': True, 'allowed': ['male', 'female']},
                    'relatives': {'type': 'list', 'minlength': 0, 'required': True, 'schema': {
                        'type': 'integer', 'min': 1, 'coerce': int}},
                }
            }
        }
    })


async def validate_by_chunks(validator, data, field, CHUNK=100):
    out_data, _errors = [], []

    while len(data):
        chunked_data = data[:CHUNK]
        data = data[CHUNK:]
        chunked_data, _e = await _validate_chunk(validator, {field: chunked_data})
        if _e:
            _errors.extend(_e)
            print(_e)
            print(chunked_data)
        else:
            out_data.extend(chunked_data[field])

    return out_data, _errors


async def _validate_chunk(validator, chunked_data):
    chunked_data = validator.normalized(chunked_data)
    _errors = _get_error_list(validator.errors)
    if _errors:
        return [], _errors
    validator.validate(chunked_data)
    _errors = _get_error_list(validator.errors)
    return chunked_data, _errors


def validate_relations(lst):
    _errors = []
    rels = []
    for c in lst:
        citizen_id = c['citizen_id']
        if not len(c['relatives']):
            continue
        relatives = list(set(c['relatives']))
        if len(c['relatives']) != len(relatives):
            _errors.append('duplicated ids found in relatives for {0}'.format(citizen_id))
        for related_citizen in relatives:
            if citizen_id < related_citizen:
                rels.append((citizen_id, related_citizen))
            elif rels.count((related_citizen, citizen_id)):
                rels.remove((related_citizen, citizen_id))
            else:
                _errors.append('{0} has single linked relation with {1}'.format(citizen_id, related_citizen))

    for citizen_id, related_citizen in rels:
        _errors.append('{0} has single linked relation with {1}'.format(citizen_id, related_citizen))

    return _errors