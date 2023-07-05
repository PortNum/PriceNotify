import sqlite3

import config


class Db:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)

    def get_conn(self):
        return self.conn

    def close_conn(self):
        self.conn.close()

    def create_table(self, table_name, fields_list):
        sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name}("
        for field in fields_list:
            sql_create_table += f"{field['name']} {field['type']},"
        sql_create_table = sql_create_table.rstrip(',') + ")"
        self.conn.execute(sql_create_table)

    def insert(self, table_name, fields, values):
        sql_insert = f"INSERT INTO {table_name} ({','.join(fields)}) VALUES ({','.join(['?'] * len(values))})"
        self.conn.execute(sql_insert, values)
        self.conn.commit()

    def delete(self, table_name, condition):
        sql_delete = f"DELETE FROM {table_name} WHERE {condition}"
        self.conn.execute(sql_delete)
        self.conn.commit()

    def update(self, table_name, set_expression, condition):
        sql_update = f"UPDATE {table_name} SET {set_expression} WHERE {condition}"
        self.conn.execute(sql_update)
        self.conn.commit()

    def select(self, table_name, fields, condition=None, limit=None):
        sql_select = f"SELECT {','.join(fields)} FROM {table_name}"
        if condition:
            sql_select += f" WHERE {condition}"
        if limit:
            sql_select += f" LIMIT {limit}"
        res = self.conn.execute(sql_select).fetchall()
        return res


def get_db():
    sqlite_db = Db(config.db_name)
    sqlite_db.create_table(config.table_name, config.field_list)
    return sqlite_db
