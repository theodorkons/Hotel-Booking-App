
import socket
from sys import base_prefix
import threading
import pickle
import rooms
import customer
from datetime import  date



HEADER = 10


def display_menu():
    print('1. Display available rooms \n 2. Book a room \n 3.Exit')


def display_rooms():
    rooms = receive()
    for room in rooms:
        print(room)


def pickle_message(message):
    msg = pickle.dumps(message)
    msg = bytes(f"{len(msg):<{HEADER}}", 'utf-8')+msg
    return msg


def check_input(answer):
    if answer =='1' or answer =='2' or answer =='3':
        return True        
    else:
        return False

def check_room_input(rooms, room_choice):
    for i in rooms:
        if str(i.get_room_number()) == room_choice:
            return True
    return False


def get_rooms():
    rooms =  receive()
    return rooms


def receive():
    while True:
        full_msg = b''
        new_msg = True
        while True:
            msg = client.recv(16)
            if new_msg:
                msglen = int(msg[:HEADER])
                new_msg = False

            full_msg += msg

            if len(full_msg)-HEADER == msglen:
                full_msg = pickle.loads(full_msg[HEADER:])
                return full_msg

def datetime_obj(date_str):
    date_str = date_str.split('/')
    date_obj = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
    return date_obj
    """ datetime_obj = datetime.strptime(date, '%y/%m/%d')
    return datetime_obj """
    


def book(rooms):
    
    room_choice = input("Which room would you like to book? ")
    while not check_room_input(rooms, room_choice):
        room_choice = input('This room does not exist, please enter a valid room number: ')
    
    client.send(pickle_message(room_choice))
    dates = receive()

    for date in dates:
        check_in = date[0].strftime('%y-%m-%d')
        check_out = date[1].strftime('%y-%m-%d')
        print(f'Unavailable dates: {check_in} to {check_out}')
    
    check_in = input('Which day would you like to check in? ')
    check_in = datetime_obj(check_in)
    check_out = input('Which day would you like to check out? ')
    check_out = datetime_obj(check_out)
    
    flag = True
    while True:
        for date in dates:
            flag = True
            if date[0] <= check_in <= date[1] or date[0] <= check_out <= date[1] or check_in <= date[0] <= check_out or check_in <= date[1] <= check_out:
                print('This room is not available during these dates. Please try again. ')
                check_in = input('Which day would you like to check in? ')
                check_in = datetime_obj(check_in)
                check_out = input('Which day would you like to check out? ')
                check_out = datetime_obj(check_out)
                flag = False
                break
        
        if flag == True:
            break
    
    client.send(pickle_message(check_in))
    client.send(pickle_message(check_out))
    
    

def registration():
    first_name = input('Please enter your first name:')
    client.send(pickle_message(first_name))
    last_name = input('Please enter your last name:')
    client.send(pickle_message(last_name))
    id_num = input('Please enter your id number:')
    client.send(pickle_message(id_num))
    birth_date = input('Please enter your birth date:')
    client.send(pickle_message(birth_date))
    phone_num = input('Please enter your phone number:')
    client.send(pickle_message(phone_num))


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

 



option = ''

while option!='3':
    display_menu()
    option = input('Choose an option: ')
    while not check_input(option):
        option = input('Please choose a valid option: ')
    
    if option=='3':
        client.close()
        exit()

    client.send(pickle_message(option))
    if option == '1':
        display_rooms()
    elif option == '2':
        answer = input('Are you a registered member? Y/N ')
        pickled_answer = pickle_message(answer)
        client.send(pickled_answer)
        if answer == 'N':
            registration()
            book()
        elif answer=='Y':
            id_num = input('Please enter your ID number:')
            client.send(pickle_message(id_num))
            cust = receive()
            i = 0
            
            if cust!= None:
                rooms = get_rooms()
                book(rooms)

            while cust == None:
                if i < 3:
                    id_num = input('This ID number does not exist, please try again: ')
                    client.send(pickle_message(id_num))
                    cust = receive()
                    i = i + 1
                else:
                    answer = input('This ID number does not exist. Press 1. to try again, 2. to register, 3. to Exit')
                    client.send(pickle_message(answer))

                    if answer == '1':
                        i = 0 
                    elif answer == '2':
                        registration()
                        book()
                        i = -1
                    elif answer == '3':
                        client.close()
                        exit()

                if i == -1:
                    break
    



            

       
        


