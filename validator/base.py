from datetime import datetime


def _validate_date(format):
    def func(f, v, e):
        try:
            if v != datetime.strptime(v, format).strftime(format):
                e(f, 'Wrong date format. Maybe...')
        except:
            e(f, 'Wrong date format. Maybe...')

    return func


def _get_error_list(validator_errors):
    return [
        '{f}: '.format(f=field) +
        '; '.join([
            '{e}'.format(e=str(err)) for err in errs
        ]) for field, errs in validator_errors.items()
    ]


class ValidationError(Exception):

    def __init__(self, validator_errors):
        super().__init__(','.join(_get_error_list(validator_errors)))
