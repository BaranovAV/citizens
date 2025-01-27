from aiohttp import web
from controller import base
from model.imports import Import as ImportModel
from validator import import_citizens
from view.imports import json_response


class Import(base.RestEndpoint):

    async def post(self):
        data, errors = await import_citizens.validate_by_chunks(import_citizens.citizens_validator(), (await self.request.json())['citizens'], 'citizens')

        import_citizens.validate_relations(data)

        if errors:
            return web.json_response({'message': errors}, status=400)

        async with self.get_connection() as a_conn:
            return json_response(await ImportModel.insert_citizen_list(data, a_conn))
