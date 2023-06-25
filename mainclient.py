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
    

    def signup(username,password,password_again) :
        ORDER = "signup"
        """signup from the client side
        [ORDER] = the order we are giving to the server to what to do
        [username] = the username that will be sent to server to check validity
        [password] = the password that will be sent to server to check validity"""
        client.send(f"('{ORDER}' ,'{str(username)}' ,'{str(password)}' ,'{str(password_again)}')".encode())
        receiver = client.recv(2048).decode()
        return receiver

    def disconnection() :
        """disconnection for the client to end its connection"""
        client.send('!DISCONNECT'.encode())
        return 0

    return (True, signin, signup, disconnection)


main_connection_to_server = connecting_to_server()

if main_connection_to_server[0] == True :
    main_connection_to_server[1]("hashembandari","lolliipopopop")
    main_connection_to_server[3]()
    