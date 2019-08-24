"""
alter table citizen
"""

from yoyo import step

__depends__ = {'20190821_01_xiXjq-add-relations'}

steps = [
    step("alter table citizens modify town varchar(255) not null", '')
]
