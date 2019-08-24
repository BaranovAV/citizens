from controller.import_citizens import ImportCitizens
from controller.imports import Import
from controller.citizens import Citizen

routes = [
    ('post', '/imports', Import.dispatch),
    ('get', '/imports/{import_id}/citizens', ImportCitizens.dispatch),
    ('patch', '/imports/{import_id}/citizen/{citizen_id}', Citizen.dispatch),
    ('get', '/imports/{import_id}/citizen/{citizen_id}', Citizen.dispatch),
]