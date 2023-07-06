import os

url = ""
secret_string = ''
headers = {"Content-Type": "application/json"}

db_name = os.path.join(os.getcwd(), "notify.db")
table_name = 'notify_list'
field_list = [
    {'name': 'id', 'type': 'INTEGER PRIMARY KEY AUTOINCREMENT'},
    {'name': 'type', 'type': 'VARCHAR(40) NOT NULL'},
    {'name': 'name', 'type': 'VARCHAR(80)'},
    {'name': 'symbol', 'type': 'VARCHAR(40) NOT NULL'},
    {'name': 'compare', 'type': 'VARCHAR(20) NOT NULL'},
    {'name': 'price', 'type': 'NUMERIC NOT NULL'},
    {'name': 'num', 'type': 'INTEGER NOT NULL'},
]

table_fields = ['type', 'name', 'symbol', 'compare', 'price', 'num']
table_fields_all = ['id', 'type', 'name', 'symbol', 'compare', 'price', 'num']

sleep_time = 10
