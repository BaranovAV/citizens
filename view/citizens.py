from aiohttp import web


def json_response(citizen):
    return web.json_response({
        'data': {
            'citizen_id': citizen['citizen_id'],
            'town': citizen['town'],
            'street': citizen['street'],
            'building': citizen['building'],
            'apartment': citizen['apartment'],
            'name': citizen['name'],
            'birth_date': citizen['birth_date'],
            'gender': citizen['gender'],
            'relatives': sorted(citizen['relatives'])
        }
    }, status=200)
