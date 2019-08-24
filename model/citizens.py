from datetime import datetime


class Citizen:

    def __init__(self, citizen_id, town, street, building, apartment, name,
                 birth_date, gender, import_id=None, relatives=None):
        birth_date = datetime.strptime(birth_date, '%d.%m.%Y')
        self.import_id = import_id
        self.citizen_id = citizen_id
        self.town = town
        self.street = street
        self.building = building
        self.apartment = apartment
        self.name = name
        self.day = birth_date.day
        self.month = birth_date.month
        self.year = birth_date.year
        self.gender = gender
        self.relatives = relatives if relatives is not None else []

    @classmethod
    def from_db(cls, **kwargs):
        kwargs['birth_date'] = datetime(year=kwargs['year'], month=kwargs['month'], day=kwargs['day']).strftime(
            '%d.%m.%Y')
        del kwargs['day']
        del kwargs['month']
        del kwargs['year']
        return cls(**kwargs)

    def add_relation(self, citizen_id):
        self.relatives.append(citizen_id)

    def to_json(self):
        return {
            'import_id': self.import_id,
            'citizen_id': self.citizen_id,
            'town': self.town,
            'street': self.street,
            'building': self.building,
            'apartment': self.apartment,
            'name': self.name,
            'birth_date': datetime(year=self.year, month=self.month, day=self.day).strftime('%d.%m.%Y'),
            'gender': self.gender,
            'relatives': self.relatives
        }
