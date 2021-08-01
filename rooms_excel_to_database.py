import mysql.connector
import xlrd

conn = mysql.connector.connect(host='localhost', user='root',passwd='root', database='hotel')

cur = conn.cursor()

cur.execute('create table if not exists rooms(RoomNo int primary key, RoomType  varchar(30), NumberofBeds int, Facilities varchar(100), Booked varchar(5))')

path = 'D:\\projects\\A star visualizer\\Rooms.xls'
a=xlrd.open_workbook(path)

sheet=a.sheet_by_index(0)

sheet.cell_value(0,0)

l=list()

for i in range(1,sheet.nrows):
    l.append(tuple(sheet.row_values(i)))

q="insert into rooms(RoomNo, RoomType, NumberofBeds, Facilities, Booked)values(%s,%s,%s,%s,%s)"
cur.executemany(q,l)
conn.commit()

conn.close()

