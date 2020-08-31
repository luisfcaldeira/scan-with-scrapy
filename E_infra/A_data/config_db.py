import os

from peewee import SqliteDatabase, PostgresqlDatabase

from E_infra.B_cross_cutting.System.errors import DBNotFound


class Config:
    dbs_names = [
        'crawling_news',
    ]

    dbs = {}

    path = ''

    def __init__(self):
        self.path = os.path.dirname(__file__)

        for db_name in self.dbs_names:
            path_db = f'{self.path}/{db_name}.db'
            self.dbs[db_name] = PostgresqlDatabase(db_name, user='postgres', password='root',
                           host='127.0.0.1', port=5432, autorollback=True)

            # self.dbs[db_name] = SqliteDatabase(path_db)

    def get_db(self, db_name):
        if db_name in self.dbs:
            return self.dbs[db_name]
        raise DBNotFound(f'Database named \'{db_name}\' was not found. Provide a valid name')

