from aiohttp import web


def json_response(import_id):
    return web.json_response({
        'data': {'import_id': import_id}
    }, status=201)
