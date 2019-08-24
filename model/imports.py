import aiomysql
from model.citizens import Citizen


class Import:

    @staticmethod
    async def get_citizen_list(import_id, conn):
        citizen_sql = 'select import_id, citizen_id, town, street, building, apartment, name, day, month, year, gender from citizens where import_id=%s', import_id
        relations_sql = 'select citizen_id, related_citizen_id from relations where import_id=%s', import_id
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(*citizen_sql)
            out_data = {c['citizen_id']: Citizen.from_db(**c) for c in await cursor.fetchall()}
            await cursor.execute(*relations_sql)
            for row in await cursor.fetchall():
                out_data[row['citizen_id']].add_relation(row['related_citizen_id'])
                out_data[row['related_citizen_id']].add_relation(row['citizen_id'])

        return [c.to_json() for c in out_data.values()]

    @staticmethod
    async def create_import(conn):
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute('insert into imports () value ()')
            return cursor.lastrowid

    @staticmethod
    async def insert_citizen_list(citizens, conn: aiomysql.Connection):
        import_id = await Import.create_import(conn)
        citizen_sql = 'insert into citizens (import_id, citizen_id, town, street, building, apartment, name, day, month, year, gender) values {0}'
        relation_sql = 'insert into relations (import_id, citizen_id, related_citizen_id) values {0}'
        citizen_values = []
        relation_values = []
        for c in citizens:
            citizen = Citizen(**c, import_id=import_id)
            citizen_values.append(
                "({import_id},{citizen_id},'{town}','{street}','{building}',{apartment},'{name}',{day},{month},{year},'{gender}')".format(
                    import_id=citizen.import_id,
                    citizen_id=citizen.citizen_id,
                    town=citizen.town,
                    street=citizen.street,
                    building=citizen.building,
                    apartment=citizen.apartment,
                    name=citizen.name,
                    day=citizen.day,
                    month=citizen.month,
                    year=citizen.year,
                    gender=citizen.gender,
                ))
            relation_values.extend([
                f"({import_id},{citizen.citizen_id},{related_citizen_id})"
                for related_citizen_id in citizen.relatives if related_citizen_id > citizen.citizen_id
            ])

        async with conn.cursor() as cursor:
            await cursor.execute(citizen_sql.format(','.join(citizen_values)))
            await cursor.execute(relation_sql.format(','.join(relation_values)))
        return import_id
