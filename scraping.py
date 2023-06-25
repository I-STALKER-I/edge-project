from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
from threading import Barrier
import requests
import pandas as pd
import pandas as pd
import io
import time

df_global = pd.DataFrame(columns=["image","discrip","price","link","market"])


def multi_extract(row, market) :
    global df_global
    while True :
        try :
            row["image"] = io.BytesIO(requests.get(row["seleniums"].find_element(By.CLASS_NAME,'w-100.radius-medium').get_attribute('src')).content)
            break
        except Exception :
            pass
    row["discrip"] = row["seleniums"].find_element(By.CLASS_NAME,'ellipsis-2.text-body2-strong').text
    row["price"] = row["seleniums"].find_element(By.CLASS_NAME,"d-flex.ai-center").text
    row["link"] = row["seleniums"].find_element(By.CLASS_NAME,"d-block.pointer.pos-relative").get_attribute('href')
    row["market"] = market
    df_global = pd.concat([df_global,row.to_frame().T],ignore_index=True)
    print(df_global)


def extract(row, market) :
    """extraxting image name bio and...etc of the product
    [row] = one of the rows in our products dataframe
    [row["image"]] = image of the product
    [row["discrip"]] = discription of the product
    [row['price']] = price of the product
    [row['link']] = link to the products page
    [row["market"]] = which market this product belongs to"""
    
    row["image"] = io.BytesIO(requests.get(row["seleniums"].find_element(By.CLASS_NAME,'w-100.radius-medium').get_attribute('src')).content)
    row["discrip"] = row["seleniums"].find_element(By.CLASS_NAME,'ellipsis-2.text-body2-strong').text
    row["price"] = row["seleniums"].find_element(By.CLASS_NAME,"d-flex.ai-center").text
    row["link"] = row["seleniums"].find_element(By.CLASS_NAME,"d-block.pointer.pos-relative").get_attribute('href')
    row["market"] = market

    return row


def divar(search):
    page = requests.get()

def outer() :
    """a closure for digikala
    [driver] = our selenium driver
    [digikala] = our digikala scraper func"""

    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    def digikala(search, page_num):
        global df_global
        """digikala will be scraped here
        [products] = our products result from the search
        [df] = a dataframe for our products"""
        driver.get(f"https://www.digikala.com/search/?page={page_num}&q={search}")
        #barrier while ,for stopping the program to proceed without loading the page
        while True :
            try :
                driver.find_element(By.CLASS_NAME,'w-100.radius-medium.d-inline-block.lazyloaded')
                break
            except Exception :
                pass

        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        products = driver.find_elements(By.CLASS_NAME,"product-list_ProductList__item__LiiNI")
        driver.execute_script("arguments[0].scrollIntoView()", products[9])
        time.sleep(1)
        df = pd.DataFrame({'seleniums' :products})
        #df.apply(extract, args=("digikala",),axis=1)
        
        threads = []
        for row in df.iterrows() :
            thread = threading.Thread(target=multi_extract,args=(row[1],"digikala"))
            thread.start()
            threads.append(thread)
        
        for thread in threads :
            thread.join()

        
        df_global.to_csv("digikala.csv")


    return digikala

digikala = outer()


def digistyle(search) :
    pass

def search_box(search) :
    pass


#https://divar.ir/s/tehran?goods-business-type=all&q=lenovo&page=6
#اول عنوانی که میخوای سرچ کنی میدی بعد صفحه رو
digikala("لپتاپ",1)