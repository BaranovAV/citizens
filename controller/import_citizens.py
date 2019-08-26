from aiohttp import web
from controller import base
from model.imports import Import
from view.import_citizens import json_response


class ImportCitizens(base.RestEndpoint):

    async def get(self, import_id):
        async with self.get_connection() as a_conn:
            import_entity = await Import.get_import(import_id, a_conn)
            if not import_entity:
                return web.json_response({'message': 'import not found'}, status=404)
            return json_response(await import_entity.get_citizen_list(a_conn))
