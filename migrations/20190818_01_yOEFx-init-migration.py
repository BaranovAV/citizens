"""
Init migration
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        '''create table citizens (
            import_id  int(10)      not null,
            citizen_id int(10)      not null,
            town       varchar(128) not null,
            street     varchar(255) not null,
            building   varchar(255) not null,
            apartment  int unsigned not null,
            name       varchar(255) not null,
            day        int(2)       not null,
            month      int(2)       not null,
            year       int(4)       not null,
            gender     varchar(8)   not null,
            primary key (import_id, citizen_id)
        ) default charset='utf8' ''', 'drop table citizens'
    )
]
