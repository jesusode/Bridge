import os
import pypyodbc

pypyodbc.win_create_mdb('.\\salesdb.mdb')

print os.path.abspath("./salesdb.mdb")

#conn = pypyodbc.connect('Driver = {Microsoft Access Driver (*. Mdb)}; DBQ =' + os.path.abspath("./salesdb.mdb"))
DRIVER={Microsoft Access Driver (*.mdb)};DBQ=c:\\dir\\file.mdb

conn = pypyodbc.connect('Driver = {Microsoft Access Driver (*. mdb)}; DBQ=C:\\Users\\jodefeb\\Desktop\\pypyodbc-1.3.3\\salesdb.mdb'

cur = conn.cursor()

cur.execute('''CREATE TABLE saleout (ID COUNTER PRIMARY KEY,customer_name VARCHAR(25), product_name VARCHAR(30), price float, volume int,sell_time datetime);''')

cur.commit()

cur.execute('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) VALUES(?,?,?,?,?)''',(u'Jiang Wen','Huawei Ascend mate',5000.5,2,'2012-1-21'))
cur.execute('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) VALUES(?,?,?,?,?)''',(u'Yang Tianzhen','Apple IPhone 5',6000.1,1,'2012-1-21'))
cur.execute('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) VALUES(?,?,?,?,?)''',(u'Zheng Xianshi','Huawei Ascend D2',5100.5,1,'2012-1-22'))
cur.execute('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) VALUES(?,?,?,?,?)''',(u'Mo Xiaomin','Huawei Ascend D2',5200.5,1,'2012-1-22'))
cur.execute('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) VALUES(?,?,?,?,?)''',(u'Gu Xiaobai','Huawei Ascend mate',5000.5,1,'2012-1-22'))

cur.commit()

cur.execute('''SELECT * FROM saleout WHERE product_name LIKE '%Huawei%''')

for d in cur.description:
    print d[0]

for row in cur.fetchall():
    for field in row: 
        print field

conn.close()