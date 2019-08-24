from aiohttp import web

from controller import base
from model.citizens import Citizen as ModelCitizen
from validator.base import ValidationError
from validator.citizens import citizen_validator
from view.citizens import json_response


class Citizen(base.RestEndpoint):

    async def patch(self, import_id, citizen_id):
        try:
            data = self._get_validated_data(citizen_validator(), await self.request.json())
        except ValidationError as e:
            return web.json_response({'message': str(e)}, status=400)
        if not data:
            return web.json_response({'message': 'no data for update'}, status=400)
        async with self.get_connection() as a_conn:
            citizen = await ModelCitizen.get_citizen(import_id, citizen_id, a_conn)
            if not citizen:
                return web.json_response({'message': 'citizen not found'}, status=404)
            citizen.update(data)
            await citizen.save(a_conn)
            return json_response(citizen.to_json())

    async def get(self, import_id, citizen_id):
        async with self.get_connection() as a_conn:
            citizen = await ModelCitizen.get_citizen(import_id, citizen_id, a_conn)
            if not citizen:
                return web.json_response({'message': 'citizen not found'}, status=404)
            return json_response(citizen.to_json())
