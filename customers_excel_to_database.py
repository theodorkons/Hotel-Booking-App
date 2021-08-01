import mysql.connector
import xlrd

conn = mysql.connector.connect(host='localhost', user='root',passwd='root', database='hotel')

cur = conn.cursor()


cur.execute('create table if not exists Customers(First_Name varchar(50), Last_Name varchar(30), Date_of_Birth date, Phone_Number bigint, ID_Number varchar(10) primary key)')

path = 'D:\\projects\\A star visualizer\\Customers.xls'
a=xlrd.open_workbook(path)

sheet=a.sheet_by_index(0)

sheet.cell_value(0,0)

l=list()

for i in range(1,sheet.nrows):
    l.append(tuple(sheet.row_values(i)))

q="insert into Customers(First_Name, Last_Name, Date_of_Birth, Phone_Number, ID_Number)values(%s,%s,%s,%s,%s)"
cur.executemany(q,l)
conn.commit()

conn.close()

