"""
add relations
"""

from yoyo import step

__depends__ = {'20190818_02_Odzpg-add-import-table'}

steps = [
    step(
        '''create table relations (
            import_id  int(10)  not null,
            citizen_id  int(10)  not null,
            related_citizen_id  int(10)  not null,
            primary key (import_id, citizen_id, related_citizen_id)
        ) default charset='utf8' ''', 'drop table relations'
    )
]
