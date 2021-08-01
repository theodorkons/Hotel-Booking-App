import mysql.connector
from rooms import Room
import customer

db = mysql.connector.connect(
host='localhost',
user='root',
passwd='root',
database='hotel'
)

mycursor = db.cursor()


def load_rooms():
    

    mycursor.execute('SELECT * FROM rooms')

    rooms = []

    for i in mycursor:
        room = Room(i[0], i[1], i[2], i[3])
        rooms.append(room)

    return rooms


def search_customer(id_num):

    mycursor.execute("SELECT * FROM CUSTOMERS WHERE ID_Number = %s", (id_num,))
    return mycursor.fetchone()


def book_room(room_num):
    
    mycursor.execute("UPDATE rooms SET Booked = 1 where RoomNo =  %s", (room_num,))
    db.commit()


def rental_dates(room_num):
    mycursor.execute("select check_in, check_out from reservations, rooms where reservations.RoomNo = rooms.RoomNo and rooms.RoomNo = %s", (room_num,))
    return mycursor.fetchall()

def add_reservation(check_in, check_out, cust, room):
    q = " INSERT INTO reservations(check_in,check_out, ID_Number, RoomNo) VALUES(%s, %s, %s, %s)"
    
    l = [check_in, check_out, cust, room]

    mycursor.execute(q,l)
    db.commit()
    


def register_customer(cust):
    insert = ("INSERT INTO customers(First_Name, Last_Name, Date_of_Birth, Phone_Number, ID_Number) VALUES(%s, %s, %s, %s, %s)")
    data = (cust.get_first_name(), cust.get_last_name(), cust.get_birth_date(), cust.get_phone_num(), cust.get_id_num())

    mycursor.execute(insert, data)
    db.commit()




# %%


import mysql.connector
from rooms import Room

db = mysql.connector.connect(
host='localhost',
user='root',
passwd='root',
database='hotel'
)

mycursor = db.cursor()

q = " INSERT INTO reservations(check_in,check_out, ID_Number, RoomNo) VALUES(%s, %s, %s, %s)"
    
l = ['2019/10/3', '2019/10/5', 'X1233', 4]
for i in l:
    print(i)
mycursor.execute(q,l)
db.commit()



# %%


""" CREATE TABLE RESERVATIONS(
id int not null auto_increment,
check_in date,
check_out date,
ID_Number varchar(10),
RoomNo int,
primary key(id),
foreign key(ID_Number) references customers(ID_Number),
foreign key(RoomNo) references rooms(RoomNo)
) """

