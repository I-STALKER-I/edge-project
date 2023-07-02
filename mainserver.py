import sqlite3
import hashlib
import socket
import threading
from threading import Lock
import json
import time
import mainpagescraper
import productloader


if __name__ == "__main__" :
    print("[LOADING] server is loading...")
    class globalisation :
        """a class for globalisation
        [mainpage] = our app's mainpage
        [is connected] = checker if the client has signedin or not"""
        #---------------------------------------------------------------------------------------------
        main_page = mainpagescraper.main()


    class client_user :
        """a class for clients whom get connected"""
        def __init__(self) :
            self.is_connected = False

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
        client = client_user()
        connected = True
        
        while connected:
            try :
                income = c.recv(1024).decode()
            except Exception :
                break

            if income:
                if income == "!DISCONNECT" :
                    connected = False
                else :
                    content = eval(income)
                    if content[0] == "signin" :
                        username ,password = content[1:]
                        password = hashlib.sha256(password.encode()).hexdigest()
                        signin(c,username,password,client)
            
                    elif content[0] == "signup" :
                        username ,password, password_again, city = content[1:]
                        password = hashlib.sha256(password.encode()).hexdigest()
                        password_again = hashlib.sha256(password_again.encode()).hexdigest()
                        signup(c,username,password,password_again,city,client)

                    elif content[0] == "searching" :
                        searching_for, page_num = content[1:]
                        search(searching_for, page_num, c)

                    elif content[0] == "product_loader" :
                        link, market = content[1:]
                        products_page_opener(link,market,c)



    def signin(c,username ,password,client) :
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
            c.send('1'.encode())
            client.is_connected = True
            #----------------------------------------------------------------------------------------------------------
            main_page_sender(c)
        else :
            c.send("0".encode())


    def signup(c,username,password,password_again,city,client) :
        """signup from the server side 
        [conn] = connection with the database
        [cur] = a control structure for traversal over the database records
        [c] = connection we have with our client
        [username] = username that was sent from client
        [password] = password that was sent from the client
        [city] = city that the person lives"""

        conn = sqlite3.connect("userdata.df")
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
        if cur.fetchall() :
            c.send("[CONFLICT] This username has been taken...".encode())
            c.send('0'.encode())
        elif password != password_again :
            #c.send("[PASSWORDINCORRECT] please enter your password correctly...")
            c.send('0'.encode())
        else :
            cur.execute("INSERT INTO userdata (username, password , city) VALUES (?, ?, ?)",(username, password, city))
            c.send("1".encode())
            client.is_connected = True
            conn.commit()
            #--------------------------------------------------------------------------------------------------------------
            main_page_sender(c)


    def main_page_sender(c) :
        """sender for mainpage
        [df_dict] = dataframe that has turned to a dict"""
        df_dict = globalisation.main_page.to_dict()
        mutex = Lock()

        def sender(dicti) :
            nonlocal c
            dicti = json.dumps(dicti)
            mutex.acquire()
            c.send(str(len(dicti)).encode())
            time.sleep(0.5)
            c.send(dicti.encode())
            mutex.release()
        sender_threads = []

        #here we are sending data multithreadly
        for key, values in df_dict.items() :
            thread = threading.Thread(target=sender,args=({key:values},))
            thread.start()
            sender_threads.append(thread)

        for thread in sender_threads :
            thread.join()

        end = json.dumps('D')
        c.send(str(len(end)).encode())
        time.sleep(0.5)
        c.send(end.encode())

    def search(searching_for,page_num,c) :
        df = mainpagescraper.scraping.multi_search(searching_for,page_num).reset_index().drop('index',axis=1)
        df_dict = df.to_dict()
        mutex = Lock()
        def sender(dicti) :
            nonlocal c
            dicti = json.dumps(dicti)
            mutex.acquire()
            c.send(str(len(dicti)).encode())
            time.sleep(0.5)
            c.send(dicti.encode())
            mutex.release()
        sender_threads = []

        #here we are sending data multithreadly
        for key, values in df_dict.items() :
            thread = threading.Thread(target=sender,args=({key:values},))
            thread.start()
            sender_threads.append(thread)

        for thread in sender_threads :
            thread.join()

        end = json.dumps('D')
        c.send(str(len(end)).encode())
        time.sleep(0.5)
        c.send(end.encode())

    def products_page_opener(link,market,c) :
        try :
            received = productloader.main(link,market)
            receive_json = json.dumps(received.to_dict())

            c.send(str(len(receive_json)).encode())
            c.send(receive_json.encode())
            return "products_page_opener successfull"
        except Exception :
            badlink = json.dumps("Bad link or market")
            c.send(str(len(badlink)).encode())
            c.send(badlink.encode())
            return "products_page_opener unsuccessful"





    while True :
        client, addr = server.accept()
        threading.Thread(target= client_handler, args = (client,)).start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
