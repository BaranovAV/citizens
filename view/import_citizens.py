from aiohttp import web


def json_response(data):

    return web.json_response({
        'data': [{
            'citizen_id': c['citizen_id'],
            'town': c['town'],
            'street': c['street'],
            'building': c['building'],
            'apartment': c['apartment'],
            'name': c['name'],
            'birth_date': c['birth_date'],
            'gender': c['gender'],
            'relatives': c['relatives']
        } for c in data]
    }, status=200)
