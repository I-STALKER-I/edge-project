from selenium import webdriver
from selenium.webdriver.common.by import By
import multiprocessing
import threading
import requests
import pandas as pd
import pandas as pd
import numpy as np
import io
import re
import time


class gloablism :
    """this class was made for global dataframes that we need
    i actually didnt wanted them to be global and instead i put them in a class
    [df_gloabl] = our gloabal dataframe
    [queue] = for getting the data from multiproccess functions"""

    df_global = pd.DataFrame(columns=["image","discrip","price","link","market"])
    df_digikala = None
    df_divar = None
    df_tecnolife = None

    if __name__ != "__main__" :
        driver = webdriver.Chrome("chromedriver.exe")


def multi_extract_tecnolife(row,market) :
    """a func for multithread extracting the data from selenium but why we would do that?
    i mean isnt using methods like apply or maybe groupby() would be faster ?
    well the answer is no because this is an io bound work and as i concluded from what i exprienced from using all of this methods
    i can say that methods like apply and groupby are way more suitble for cpu bound works
    but in here we have an io bound work that needs multithreading and it is the  efficent way
    [row] = row of our pandas dataframe df
    [row['image']] = the image column of our global dataframe that is a io.Bytes
    [row['discrip']] = discription of our product
    [row['price']] = price of our product
    [row['link']] = link to the product's web page
    [row['market']] = what market the product belongs to
    UPDATE : element finding was multithreaded every element has a new thread
    [thread_image] = thread for products image
    [thread_discrip] = thread for finding products discription
    [thread_price] = finding products price
    [thread_link] = finding products links"""

    thread_image = threading.Thread(target=image_tecnolife,args=(row,))
    thread_image.start()
    thread_discrip = threading.Thread(target=discrip,args=(row, 'ProductComp_product_title__bOrf5'))
    thread_discrip.start()
    thread_price = threading.Thread(target=price_digikala_tecnolife,args=(row, 'ProductComp_main_price__XgWce'))
    
    thread_price.start()
    thread_link = threading.Thread(target= link_digikala_tecnolife,args=(row,'ProductComp_product_title__bOrf5'))
    thread_link.start()

    thread_image.join()
    thread_discrip.join()
    thread_link.join()
    thread_price.join()
    row['market'] = market
    regularexpression(row)
    

    gloablism.df_global = pd.concat([gloablism.df_global,row.to_frame().T],ignore_index=True) 



def multi_extract_divar(row, market, index) :
    """a func for multithread extracting the data from selenium but why we would do that?
    i mean isnt using methods like apply or maybe groupby() would be faster ?
    well the answer is no because this is an io bound work and as i concluded from what i exprienced from using all of this methods
    i can say that methods like apply and groupby are way more suitble for cpu bound works
    but in here we have an io bound work that needs multithreading and it is the  efficent way
    [row] = row of our pandas dataframe df
    [row['image']] = the image column of our global dataframe that is a io.Bytes
    [row['discrip']] = discription of our product
    [row['price']] = price of our product
    [row['link']] = link to the product's web page
    [row['market']] = what market the product belongs to
    UPDATE : element finding was multithreaded every element has a new thread
    [thread_image] = thread for products image
    [thread_discrip] = thread for finding products discription
    [thread_price] = finding products price
    [thread_link] = finding products links"""
    thread_image = threading.Thread(target=image,args=(row,"kt-image-block__image"))
    thread_image.start()
    thread_discrip = threading.Thread(target=discrip,args=(row,'kt-post-card__title'))
    thread_discrip.start()
    thread_price = threading.Thread(target=price_divar,args=(row,))
    thread_price.start()
    thread_link = threading.Thread(target=link_divar,args=(row,index))
    thread_link.start()


    thread_image.join()
    thread_discrip.join()
    thread_link.join()
    thread_price.join()
    row['market'] = market
    regularexpression(row)

    gloablism.df_global = pd.concat([gloablism.df_global,row.to_frame().T],ignore_index=True)

def image_tecnolife(row) :
    counter = 0
    while True :
        counter += 1
        try :
            row["image"] = row['seleniums'].find_element(By.CLASS_NAME,"ProductComp_product_image__JBXYv").find_element(By.TAG_NAME,'img').get_attribute('src')
            break
        except Exception :
            pass

        if counter >= 10 :
            row["image"] = np.nan
            break
            
def image(row,class_name) :
    counter =  0
    while True :
        counter += 1
        try :
            row["image"] = row["seleniums"].find_element(By.CLASS_NAME,class_name).get_attribute('src')
            break
        except Exception :
            pass


        if counter >= 10 :
            row["image"] = np.nan
            break

def discrip(row,class_name) :
    try :
        row["discrip"] = row["seleniums"].find_element(By.CLASS_NAME,class_name).text
    except Exception :
        try :
            row["discrip"] = np.nan
        except Exception :
            row["discrip"] = pd.Series(np.nan)

def price_divar(row) :

    try :
        row["price"] = row["seleniums"].find_elements(By.CLASS_NAME,"kt-post-card__description")[1].text
    except Exception :
        row["price"] = np.nan

def link_divar(row,index) :
    try :
        row["link"] = row["seleniums"].find_element(By.CSS_SELECTOR,f'#app > div.kt-col-md-12-d59e3.browse-c7458 > main > div > div > div > div > div:nth-child({index}) > a').get_attribute('href')
    except Exception :
        row["link"] = np.nan
def price_digikala_tecnolife(row,class_name) :
    try :
        row["price"] = row["seleniums"].find_element(By.CLASS_NAME,class_name).text
    except Exception :
        row['price'] = np.nan

def link_digikala_tecnolife(row,class_name) :
    try :
        row["link"] = row["seleniums"].find_element(By.CLASS_NAME,class_name).get_attribute('href')
    except Exception :
        row['link'] = np.nan

def multi_extract_digikala(row, market) :
    """a func for multithread extracting the data from selenium but why we would do that?
    i mean isnt using methods like apply or maybe groupby() would be faster ?
    well the answer is no because this is an io bound work and as i concluded from what i exprienced from using all of this methods
    i can say that methods like apply and groupby are way more suitble for cpu bound works
    but in here we have an io bound work that needs multithreading and it is the  efficent way
    [row] = row of our pandas dataframe df
    [row['image']] = the image column of our global dataframe that is a io.Bytes
    [row['discrip']] = discription of our product
    [row['price']] = price of our product
    [row['link']] = link to the product's web page
    [row['market']] = what market the product belongs to
    UPDATE : element finding was multithreaded every element has a new thread
    [thread_image] = thread for products image
    [thread_discrip] = thread for finding products discription
    [thread_price] = finding products price
    [thread_link] = finding products links"""

    thread_image = threading.Thread(target=image,args=(row,'w-100.radius-medium'))
    thread_image.start()
    thread_discrip = threading.Thread(target=discrip,args=(row, 'ellipsis-2'))
    thread_discrip.start()
    thread_price = threading.Thread(target=price_digikala_tecnolife,args=(row,"d-flex.ai-center.jc-end"))
    thread_price.start()
    thread_link = threading.Thread(target= link_digikala_tecnolife,args=(row,"d-block.pointer.pos-relative"))
    thread_link.start()

    thread_image.join()
    thread_discrip.join()
    thread_link.join()
    thread_price.join()
    row['market'] = market
    regularexpression(row)

    gloablism.df_global = pd.concat([gloablism.df_global,row.to_frame().T],ignore_index=True) 

def regularexpression(row) :
    string = row['discrip']
    if type(string) == str :
        if re.search('مدل',string) :
            model = re.findall('^[\w]+(?=\s)',string)[0].strip()
            try :
                product_discription = re.findall('(?<=مدل)\s([a-zA-Z-.\s\d]+)(?=[\s\w])',string)[0].strip()
                row["indexer"] = model + product_discription

            except Exception :
                row["indexer"] = row["discrip"]
        
        else :
            row["indexer"] = row["discrip"]



def divar(search, page_num,queue,city="tehran"):
        """divar will be scraped here
        [products] = our products result from the search
        [df] = a dataframe for our products
        [search] = what we are searching for
        [page_num] = page number of site we want to scrape(a result of search has more than one page so we have to know which  page we want)
        [city] = the city client lives in (divar asks for the city)
        [gloablism.driver] = our selenium driver
        [threads] = threads we are making for concurrency
        [df_dict] = convertion of gloablism.df_global to a dictionary so we can queue it"""
        gloablism.driver.maximize_window()
        #gloablism.driver.minimize_window()
        gloablism.driver.get(f"https://divar.ir/s/{city}?goods-business-type=all&q={search}&page={page_num}")
        try :
            products = gloablism.driver.find_elements(By.CLASS_NAME,"post-card-item-af972.kt-col-6-bee95")
        except Exception :
            queue.put("N")
            queue.put("D")
            queue.close()
            print("No products for divar!")
            return 0

        if len(products) == 0 :
            queue.put("N")
            queue.put("D")
            queue.close()
            print("No products for divar!")
            return 0
        df = pd.DataFrame({'seleniums' :products})

        threads = []
        for i,row in enumerate(df.iterrows()) :
            thread = threading.Thread(target=multi_extract_divar, args=(row[1] ,"divar",i+1))
            thread.start()
            threads.append(thread)
        
        for thread in threads :
            thread.join()

        gloablism.df_global.drop("seleniums",inplace=True,axis=1)
        df_dict = gloablism.df_global.to_dict()
        sender_threads = []
        for key ,values in df_dict.items() :
            thread = threading.Thread(target=sender, args=(queue,{key:values}))
            thread.start()
            sender_threads.append(thread)

        for thread in sender_threads :
            thread.join()

        queue.put("D")
        queue.close()
        print("Divar is completely Done!")


def sender(queue,dicti) :
    """a func for sending multithreadly
    [queue] = queue for sending data
    [dicti] = the dictionary that is going to be sent"""
    queue.put(dicti)


def digikala(search, page_num,queue):
        """digikala will be scraped here
        [search] = what we are searching for
        [page_num] = page number of site we want to scrape(a result of search has more than one page so we have to know which  page we want)
        [products] = our products result from the search
        [df] = a dataframe for our products
        [gloablism.driver] = our selenium driver
        [threads] = threads we are making for concurrency
        [df_dict] = convertion of gloablism.df_global to a dictionary so we can queue it
        """
        gloablism.driver.maximize_window()
        #gloablism.driver.minimize_window()
        gloablism.driver.get(f"https://www.digikala.com/search/?has_selling_stock=1&page={page_num}&q={search}")
        #barrier while ,for stopping the program to proceed without loading the page
        counter = 0
        while True :
            counter += 1
            try :
                gloablism.driver.find_element(By.CLASS_NAME,'w-100.radius-medium.d-inline-block.lazyloaded')
                break
            except Exception :
                pass

            if counter >= 30 :
                break

        try :
            products = gloablism.driver.find_elements(By.CLASS_NAME,"product-list_ProductList__item__LiiNI")
        except Exception :
            queue.put("N")
            queue.put("D")
            queue.close()
            print("No products for Digikala!")
            return

        if len(products) == 0 :
            queue.put("N")
            queue.put("D")
            queue.close()
            print("No products for Digikala!")
            return 0

        gloablism.driver.execute_script("arguments[0].scrollIntoView()", products[len(products)//2])
        time.sleep(1)
        df = pd.DataFrame({'seleniums' :products})
        
        threads = []
        for row in df.iterrows() :
            thread = threading.Thread(target=multi_extract_digikala,args=(row[1], "digikala"))
            thread.start()
            threads.append(thread)
        
        for thread in threads :
            thread.join()

        gloablism.df_global.drop("seleniums",inplace=True,axis=1)

        df_dict = gloablism.df_global.to_dict()
        sender_threads = []

        #here we are sending data multithreadly
        for key, values in df_dict.items() :
            thread = threading.Thread(target=sender,args=(queue,{key:values}))
            thread.start()
            sender_threads.append(thread)

        for thread in sender_threads :
            thread.join()

        #this is for telling the receiver that we are done sending
        queue.put("D")
        queue.close()
        print("Digikala is completely done!")

def tecnolife(search, page_num, queue) :
    """technolife will be scraped here
    [search] = what we are searching for
    [page_num] = page number of site we want to scrape(a result of search has more than one page so we have to know which  page we want)
    [products] = our products result from the search
    [df] = a dataframe for our products
    [gloablism.driver] = our selenium driver
    [threads] = threads we are making for concurrency
    [df_dict] = convertion of gloablism.df_global to a dictionary so we can queue it"""

    gloablism.driver.maximize_window()
    #gloablism.driver.minimize_window()
    gloablism.driver.get(f"https://www.technolife.ir/product/list/search?keywords={search}&page={page_num}&only_available=true")
    #barrier while ,for stopping the program to proceed without loading the page
   #while True :
        #try :
        #    gloablism.driver.find_element(By.CLASS_NAME,'ProductComp_product_image__JBXYv')
        #    break
        #except Exception :
        #    pass

    try :
        products = gloablism.driver.find_elements(By.CLASS_NAME, "ProductPrlist_product__PdoZm")
    except Exception :
        queue.put("N")
        queue.put("D")
        queue.close()
        print("No products for tecnolife!")
        return 0

    if len(products) == 0 :
        queue.put("N")
        queue.put("D")
        queue.close()
        print("No products for tecnolife!")
        return 0
    gloablism.driver.execute_script("arguments[0].scrollIntoView()", products[len(products)//2])
    time.sleep(1)
    df = pd.DataFrame({'seleniums' :products})
        
    threads = []
    for row in df.iterrows() :
        thread = threading.Thread(target=multi_extract_tecnolife,args=(row[1], "tecnolife"))
        thread.start()
        threads.append(thread)
        
    for thread in threads :
        thread.join()

    gloablism.df_global.drop("seleniums",inplace=True,axis=1)

    df_dict = gloablism.df_global.to_dict()
    sender_threads = []

    #here we are sending data multithreadly
    for key, values in df_dict.items() :
        thread = threading.Thread(target=sender,args=(queue,{key:values}))
        thread.start()
        sender_threads.append(thread)

    for thread in sender_threads :
        thread.join()

    #this is for telling the receiver that we are done sending
    queue.put("D")
    queue.close()
    print("tecnolife is completely done!")

    #https://www.technolife.ir/product/list/search?keywords=lenovo&page=2


def reciever(queue, market) :
    """a function for receiving multithreaded sendings
    [dictionary] = a dictionary to put all the things we received in it
    [income] = incoming from sender
    """
    dictionary = {}
    while True :
        income = queue.get()
        if income == "D" :
            break

        elif income == "N" :
            dictionary = {'image':[np.nan],'discrip' : [np.nan],'price' : [np.nan], 'link' : [np.nan],'market' : [np.nan]}
            pass            

        else :
            dictionary[list(income.keys())[0]] = list(income.values())[0]

    if market == "digikala" :
        gloablism.df_digikala = pd.DataFrame(dictionary)
    elif market == "divar" :
        gloablism.df_divar = pd.DataFrame(dictionary)
    else :
        gloablism.df_tecnolife = pd.DataFrame(dictionary)

            

def multi_search(search,page_num) :
    """a function for concurrent searching in all sites
    the two main proccess we have in here,digikala scraping
    and divar scraping are now being proccessed concurrently
    and theye're proccesseses instead of threads 
    the queue is a solution to the problem of not getting
    a return from proccess,the main problem with this work is that
    sending  and receiving big data would take time we made a solution
    for it by breaking the data into chunks and sending them multithreadly
    to the receiver(multithread because i think that this is an IO band work)
    [queue_1] = first qeueue from multiproccessing
    [queue_2] = second queue for multiproccessing
    [digikala_thread] = a proccess for scraping digikala
    [divar_thread] = a proccesss for scraping divar
    [receiving_thread_digi] = a receiver thread for queue_1
    [receiving_thread_divar] = a receiver thread for the queue_2

    [df_glob] = a global dataframe"""
    queue_2 = multiprocessing.Queue() 
    queue_1 = multiprocessing.Queue()
    queue_3 = multiprocessing.Queue()
    digikala_thread = multiprocessing.Process(target=digikala, args=(search,page_num,queue_1))
    divar_thread = multiprocessing.Process(target=divar, args = (search,page_num,queue_2))
    tecnolife_thread = multiprocessing.Process(target=tecnolife,args=(search,page_num,queue_3))
    digikala_thread.start()
    divar_thread.start()
    tecnolife_thread.start()
    
    receiving_thread_digi = threading.Thread(target=reciever,args=(queue_1,"digikala"))
    receiving_thread_divar = threading.Thread(target=reciever,args=(queue_2,"divar"))
    receiving_thread_tecnolife = threading.Thread(target=reciever,args=(queue_3,"tecnolife"))
    receiving_thread_digi.start()
    receiving_thread_divar.start()
    receiving_thread_tecnolife.start()

    receiving_thread_divar.join()
    receiving_thread_digi.join()
    receiving_thread_tecnolife.join()

    df_digikala_divar = pd.concat([gloablism.df_digikala,gloablism.df_divar])
    #df_digikala_divar = pd.merge(gloablism.df_digikala, gloablism.df_divar, how='outer')
    #df_glob = pd.merge(df_digikala_divar,gloablism.df_tecnolife,how='outer')
    df_glob = pd.concat([df_digikala_divar,gloablism.df_tecnolife])
    return df_glob.dropna().reset_index().reset_index().drop('index',axis=1).set_index(['indexer','level_0'])

def helper() :
    """for using this module
    the main function is multi_search
    that takes two parameters
    first : what we want to search and it has to be a string
    second : a number or integer for the page_number
    i have written many docs you can read. 
    it will bright many things for you """


if __name__ == '__main__' :
    help(helper)
