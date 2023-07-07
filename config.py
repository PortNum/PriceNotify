import os

url = "https://open.feishu.cn/open-apis/bot/v2/hook/57dfbb83-ca88-42f1-81e5-89e75eb6b2eb"
secret_string = 'C2YJrXQC5uN4I3zW6VwTAc'
headers = {"Content-Type": "application/json"}

db_name = os.path.join(os.getcwd(), "notify.db")
log_name = os.path.join(os.getcwd(), "notify.log")
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
