import inspect
from aiohttp import web
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from multidict import MultiDict

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')


class RestEndpoint:
    _user = None

    def _get_validated_data(self, validator, data):
        data = validator.normalized(data)
        if not (data is not None and validator.validate(data)):
            raise Exception(
                '\n'.join([
                    '{f}: '.format(f=field) +
                    '; '.join([
                        '{e}'.format(e=str(err)) for err in errs
                    ]) for field, errs in validator.errors.items()
                ])
            )
        return data

    def get_connection(self):
        return self.request.app['db_pool'].acquire()

    @staticmethod
    def json_response(func):
        async def wrapped(*args, **kwargs):
            return web.json_response(await func(*args, **kwargs))

        return wrapped

    @staticmethod
    def file_response(*, headers, content_type='application/octet-stream'):
        def decorator(func):
            async def wrapped(*args, **kwargs):
                data = await func(*args, **kwargs)

                resp = web.StreamResponse(headers=MultiDict(headers))
                resp.content_type = content_type
                resp.content_length = len(data)
                await resp.prepare(args[0].request)
                await resp.write(data)

                return resp

            return wrapped

        return decorator

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
