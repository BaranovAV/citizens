from controller.get_citizens import Citizens
from controller.import_citizens import CitizensInImport

routes = [
    ('post', '/imports', CitizensInImport.dispatch),
    ('get', '/imports/{import_id}/citizens', Citizens.dispatch),
]