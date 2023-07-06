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


def delete_task(id):
    db_for_delete = get_db()
    db_for_delete.delete(config.table_name, "id=%s" % id)
    db_for_delete.close_conn()


def update_task(id: int, num: int):
    try:
        if num == 0 or num - 1 == 0:
            delete_task(id)
            return
        num = num - 1
        db = get_db()
        set_sql = "num=%d" % num
        where_sql = "id=%d" % id
        db.update(config.table_name, set_sql, where_sql)
        db.close_conn()
    except Exception as e:
        print(e)
        return None


def list_task():
    db = get_db()
    rows = db.select(config.table_name, config.table_fields_all)
    print("%-8s%-15s%-8s%-10s%-8s%-8s%-8s%-8s" % (
        "ID", "类型", "名称", "代码", "高于/低于", "价格", "剩余通知次数", "是否通知"))
    for r in rows:
        print("%-8s%-15s%-8s%-10s%-8s%-8s%-8s%-8s" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
    db.close_conn()
