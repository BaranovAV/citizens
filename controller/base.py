import inspect
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from validator.base import ValidationError

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')


class RestEndpoint:
    _user = None

    def _get_validated_data(self, validator, data):
        data = validator.normalized(data)
        if not (data is not None and validator.validate(data)):
            raise ValidationError(validator.errors)
        return data

    def get_connection(self):
        return self.request.app['db_pool'].acquire()

    def __init__(self, request):
        self.methods = {}
        self.request = request

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    @classmethod
    async def dispatch(cls, request: Request):
        self = cls(request)
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            raise HttpBadRequest('Expected match info that does`t exist: {}'.format(','.join(unsatisfied_args)))

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})
