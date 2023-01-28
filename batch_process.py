import csv
from datetime import datetime

import mysql.connector


mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password="password"
)

cur = mydb.cursor()
cur.execute("USE deutsche_bahn")


data_file = 'orders.csv'

with open(data_file, "r") as f:
    csv_reader = csv.DictReader(f)
    records = list(csv_reader)


for record in records:
    print(record)
    order_time = record['order_time']
    date_obj = datetime.strptime(order_time, '%Y-%m-%d %H:%M:%S.%f')
    item = record['item']
    sql_stmt = f"INSERT INTO Orders(OrderTime, Item) VALUES('{date_obj}', '{item}')"
    cur.execute(sql_stmt)
    mydb.commit()

cur.close()
mydb.close()