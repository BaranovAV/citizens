from controller import base
from model.imports import Import
from view.import_citizens import json_response


class ImportCitizens(base.RestEndpoint):

    async def get(self, import_id):
        async with self.get_connection() as a_conn:
            return json_response(await Import.get_citizen_list(import_id, a_conn))
