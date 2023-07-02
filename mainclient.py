import socket
import json
import pandas as pd

class globalisation :
    """a class for globalisation
    [main_page] = main_page of site"""
    is_connected = False
    main_page = None


def connecting_to_server() :
    """make sures that the client is connected to the server
    [client] = A subclass of _socket.socket(for more info type help(client))"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        client.connect(("localhost", 9999))
    except Exception :
        print("Error [connection to the server failed]")
        return (False,"[connection to the server failed]")


    def signin(username,password) :
        ORDER = "signin"
        """signin from the client side
        [username] = the username that will be sent to server to check validity
        [password] = the password that will be sent to server to check validity
        [ORDER] = the order we are giving to the server to what to do
        [signin] = a def for signing in
        [signup] = a def for signing up
        [disconnection] = a def for disconnecting"""
        client.send(f"('{ORDER}' ,'{str(username)}' ,'{str(password)}')".encode())
        receiver = client.recv(2048).decode()
        return receiver
    

    def signup(username,password,password_again,city) :
        ORDER = "signup"
        """signup from the client side
        [ORDER] = the order we are giving to the server to what to do
        [username] = the username that will be sent to server to check validity
        [password] = the password that will be sent to server to check validity"""
        client.send(f"('{ORDER}' ,'{str(username)}' ,'{str(password)}' ,'{str(password_again)}' ,'{str(city)}')".encode())
        receiver = client.recv(2048).decode()
        return receiver

    def disconnection() :
        """disconnection for the client to end its connection"""
        client.send('!DISCONNECT'.encode())
        return 0
    
    def main_page() :
        """a function for receiving multithreaded sendings
        [dictionary] = a dictionary to put all the things we received in it
        [income] = incoming from sender    """
        dictionary = {}
        while True :
            message_length = client.recv(64).decode()
            income = client.recv(int(message_length))
            if income :
                income = json.loads(income.decode())
                if income == "D" :
                    break    

                else :
                    dictionary[list(income.keys())[0]] = list(income.values())[0]

        
        return pd.DataFrame(dictionary)
    

    def search(searching_for,page_num) :
        """a fucntion for searching
        [client] = the user client
        [dictionary] = a dictionary to put our json's in it
        [income] = incoming json from server
        [message_length] = incoming message length"""
        client.send(f"('searching', '{searching_for}', '{page_num}')".encode())
        dictionary = {}
        while True :
            message_length = client.recv(64).decode()
            income = client.recv(int(message_length))
            if income :
                income = json.loads(income.decode())
                if income == "D" :
                    break    

                else :
                    dictionary[list(income.keys())[0]] = list(income.values())[0]

        return pd.DataFrame(dictionary)


    return (True, signin, signup, disconnection, main_page, search)




def main(order,username=None,password=None,password_again=None,city=None,searching_for = None,page_num = None) :
    '''the main function that controls client
    [order] = the order to do (signin or signup)
    [username] = username of client
    [password] = password of client
    [password_again] = one of the signup requirments that has to be given'''
    main_connection_to_server = connecting_to_server()
    if main_connection_to_server[0] == True :
        
        #signin = main_connection_to_server[1]
        #signup = main_connection_to_server[2]
        #disconnect = main_connection_to_server[3] 
        #main_page_receiver = main_connection_to_server[4]
        #search = main_connection_to_server[5]

        if order == 'signin':
            receiver =  main_connection_to_server[1](username,password)
            if receiver == '1' :
                globalisation.main_page = main_connection_to_server[4]()
                globalisation.is_connected = True
                pass
                    
            else :
                return 0
        elif order == 'signup' :
            receiver = main_connection_to_server[2](username,password,password_again,city)
            if receiver == '1' :
                globalisation.main_page = main_connection_to_server[4]()
                globalisation.is_connected = True
                return 1
            else :
                return 0
            
        

        elif order == "disconnect" :
            main_connection_to_server[3]()

        elif order == "search" :
                if globalisation.is_connected == True :
                    return main_connection_to_server[5](searching_for, page_num) 
                
                else :
                    return 0
        
        else :
            raise ValueError

    else :
        return 0
    
def helper() :
    """HELP:
    the head function is 'main' that controls the client
    for using this module you have to use 'main' function passing it
    the requirments,first you have to give the order you want ('signin' or 'signup') as string
    then giving it the username and password remember for signing up you have to give him a password again
    it would be like this if we want to signin == main('signin','I-STALKER-I','123456789')
    remember that mainserver has to be running so this module works because if there is no sever then there is no connection
    so the client could connect"""

if __name__ == '__main__' :
    help(helper)
    print(main("signin",'sinakhol1382','SiNagol1382'))
    globalisation.main_page.to_csv("main_page.csv")
    
    print(main("search",searching_for='لپتاپ',page_num=1))
    main("disconnect")