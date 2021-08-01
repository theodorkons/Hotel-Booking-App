#import client
import socket
import threading
import rooms
import mysql.connector
import queries
import pickle
import select
import customer


HOST = '127.0.0.1'
PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 10
FORMAT = 'utf-8'


def check_input(answer):
    if answer!='1' or answer!='2' or answer!='3':
        return False
    else:
        return True

def pickle_message(message):
    msg = pickle.dumps(message)
    msg = bytes(f"{len(msg):<{HEADER}}", 'utf-8')+msg
    return msg



def send_customer(cust):
    if cust == None:
        conn.send(pickle_message(cust))
    else:
        cust = customer.Customer(cust[0], cust[1], cust[2], cust[3], cust[4])
        conn.send(pickle_message(cust))
    


def rooms():
    rooms = queries.load_rooms()
    msg = pickle_message(rooms)
    conn.send(msg)


def book(cust):
    
    room_choice = receive()
    dates = queries.rental_dates(room_choice)
    msg = pickle_message(dates)
    conn.send(msg)
    check_in = receive()
    check_out = receive()
    print(check_in, check_out, cust, room_choice)
    queries.add_reservation(check_in, check_out, cust, room_choice)
    

def registration():
    first_name = receive()
    last_name =  receive()
    id_num = receive()
    birth_date = receive()
    phone_num = receive()
    cust = customer.Customer(first_name, last_name, birth_date, phone_num, id_num)
    return cust

def receive():
    while True:
        full_msg = b''
        new_msg = True
        while True:                                            #buffering message
            msg = conn.recv(16)
            if new_msg:
                msglen = int(msg[:HEADER])
                new_msg = False

            full_msg += msg


            if len(full_msg)-HEADER == msglen:
                full_msg = pickle.loads(full_msg[HEADER:])
                return full_msg

def handle_client(conn,addr):
    
    client_option = receive()
    
    while client_option != '3':

        if client_option == '1':
            rooms()
        elif client_option =='2':
            answer = receive()
            if answer == 'N':
                cust = registration()
                book()
            elif answer == 'Y':
                id_num = receive()
                cust = queries.search_customer(id_num)
                send_customer(cust)
                if cust != None:
                    rooms()
                    book(cust)
               
                i = 0
                while cust == None:  
                    if i < 3:
                        id_num = receive()
                        cust = queries.search_customer(id_num)
                        send_customer(cust)
                        i = i + 1
                    else:
                        answer = receive()
                        if answer == '1':
                            i = 0
                        elif answer == '2':
                            cust = registration()
                            book(cust)
        
            
            
            

            

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[LISTENING] Server is listening on {SERVER}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))         #starting server
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    

