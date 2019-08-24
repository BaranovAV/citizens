"""
add import table
"""

from yoyo import step

__depends__ = {'20190818_01_yOEFx-init-migration'}

steps = [
    step(
        '''create table imports (
            import_id  int(10)  not null auto_increment,
            create_dt  datetime default now(),
            primary key (import_id)
        ) default charset='utf8' ''', 'drop table imports'
    )
]
