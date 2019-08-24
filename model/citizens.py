from datetime import datetime
import aiomysql


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

    @classmethod
    async def get_citizen(cls, import_id, citizen_id, conn: aiomysql.Connection):
        citizen_sql = 'select import_id, citizen_id, town, street, building, apartment, name, day, month, year, gender from citizens.citizens where import_id = %s and citizen_id = %s', (
            import_id, citizen_id)
        relates_sql = 'select related_citizen_id as relative from citizens.relations where import_id = %s and citizen_id = %s union all select citizen_id as relative from citizens.relations where import_id = %s and related_citizen_id = %s', (
            import_id, citizen_id, import_id, citizen_id)
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(*citizen_sql)
            citizen = await cursor.fetchone()
            if not citizen:
                return None
            await cursor.execute(*relates_sql)
            relates = await cursor.fetchall()
            return cls.from_db(**citizen, relatives=[r['relative'] for r in relates])

    def add_relation(self, citizen_id):
        self.relatives.append(citizen_id)

    def update(self, new_data):
        if 'birth_date' in new_data:
            birth_date = datetime.strptime(new_data['birth_date'], '%d.%m.%Y')
            new_data['day'] = birth_date.day
            new_data['month'] = birth_date.month
            new_data['year'] = birth_date.year
            del new_data['birth_date']
        for param, value in new_data.items():
            setattr(self, param, value)

    async def save(self, conn):
        update_citizen = \
            'update citizens.citizens set town=%s, street=%s, building=%s, ' \
            'apartment=%s, name=%s, day=%s, month=%s, year=%s, gender=%s ' \
            'where import_id=%s and citizen_id=%s', \
            (self.town, self.street, self.building, self.apartment, self.name,
             self.day, self.month, self.year, self.gender, self.import_id,
             self.citizen_id)
        remove_relatives = 'delete from citizens.relations where import_id=%s and (citizen_id=%s or related_citizen_id=%s)', (
            self.import_id, self.citizen_id, self.citizen_id)
        insert_relatives = None
        if len(self.relatives):
            insert_relatives = 'insert into relations (import_id, citizen_id, related_citizen_id) values {0}'.format(
            ', '.join(
                [
                    f"({self.import_id},{related_citizen_id},{self.citizen_id})"
                    for related_citizen_id in self.relatives if related_citizen_id < self.citizen_id
                ] + [
                    f"({self.import_id},{self.citizen_id},{related_citizen_id})"
                    for related_citizen_id in self.relatives if related_citizen_id > self.citizen_id
                ]))

        async with conn.cursor() as cursor:
            await cursor.execute(*update_citizen)
            await cursor.execute(*remove_relatives)
            if len(self.relatives):
                await cursor.execute(insert_relatives)

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
