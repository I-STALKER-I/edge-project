import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",9999))
server.listen()
print("[LISTENING] server is listening...")

def client_handler(c) :
    """client will be handled here meaning that everything that has to be sent to it and anything that has to 
    be recieved here will be handled
    [c] = the connection"""
    #c.send("Username: ".encode())
    #username = c.recv(1024).decode()
    #c.send("Password: ".encode())
    #password = c.recv(1024)
    
    connected = True
    while connected:
        income = c.recv(1024).decode()
        if income:
            if income == "!DISCONNECT" :
                connected = False
            else :
                content = eval(income)
                if content[0] == "signin" :
                    username ,password = content[1:]
                    password = hashlib.sha256(password.encode()).hexdigest()
                    signin(c,username,password)
                
                elif content[0] == "signup" :
                    username ,password, password_again = content[1:]
                    password = hashlib.sha256(password.encode()).hexdigest()
                    password_again = hashlib.sha256(password_again.encode()).hexdigest()
                    signup(c,username,password,password_again)#password again


def signin(c,username ,password) :
    """signin from the server side 
    [conn] = connection with the database
    [cur] = a control structure for traversal over the database records
    [c] = connection we have with our client
    [username] = username that was sent from client
    [password] = password that was sent from the client"""

    conn = sqlite3.connect("userdata.df")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ? and password = ?", (username,password))
    if cur.fetchall() :
        c.send(f"Login for {c.getpeername()[0]} was successful".encode())
    else :
        c.send("Login failed!".encode())


def signup(c,username,password,password_again) :
    """signup from the server side 
    [conn] = connection with the database
    [cur] = a control structure for traversal over the database records
    [c] = connection we have with our client
    [username] = username that was sent from client
    [password] = password that was sent from the client"""

    conn = sqlite3.connect("userdata.df")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    if cur.fetchall() :
        c.send("[CONFLICT] This username has been taken...".encode())
    else :
        cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)",(username,password))
        c.send("Signup successfull!".encode())
        conn.commit()

while True :
    client, addr = server.accept()
    threading.Thread(target= client_handler, args = (client,)).start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
