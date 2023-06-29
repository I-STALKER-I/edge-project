import socket
def connecting_to_server() :
    """make sures that the client is connected to the server
    [client] = A subclass of _socket.socket(for more info type help(client))"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        client.connect(("localhost", 9999))
    except Exception :
        print("Error [connection to the server failed]")
        return (False,"[connection to the server failed]")
    #message = client.recv(1024).decode()
    #client.send(input(message).encode())
    #message = client.recv(1024).decode()
    #client.send(input(message).encode())
    #print(client.recv(1024).decode())
    #



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

    return (True, signin, signup, disconnection)




def main(order,username,password,password_again=None,city=None) :
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

        if order == 'signin':
            print(main_connection_to_server[1](username,password))
            main_connection_to_server[3]()
            return 1
        elif order == 'signup' :
            print(main_connection_to_server[2](username,password,password_again,city))
            main_connection_to_server[3]()
            return 1

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