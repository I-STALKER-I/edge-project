from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import re




def main(address,market) :
    """the main function for scraping products page
    [address] = products link address
    [market] = product's market"""
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    driver.get(address)

    if market == "digikala" :
        return digikala(driver)

    elif market == "divar" :
        return divar(driver)

    else :
        return tecnolife(driver)

def digikala(driver) :
    """for products in digikala market
    [bio] = bio of product
    [properties] = properties of product
    [template] = template that properties lie there
    [properties_list] = list of propertes texts
    """
    while True :
        try :
            bio = driver.find_element(By.CLASS_NAME,'text-h4.color-900').text
            if len(bio) > 0 :
                break
        except Exception :
            pass
    
    try :
        template = driver.find_element(By.CLASS_NAME,'mx-5.mx-0-lg.pb-3-lg.styles_InfoSection__wrapper__e2TLb.border-b.pb-1')
        properties = template.find_elements(By.CLASS_NAME,'d-flex.ai-center.mb-1')
        properties_list = []
        for properti in properties :
            properties_list.append(repr(properti.text).replace('\\u200c','').replace('\\n',''))

    except Exception :
        print("[NAN] no properties")
        properties_list = []

    try :
        price = driver.find_element(By.CLASS_NAME,'color-800.ml-1.text-h4').text
    except Exception :
        try :
            price = driver.find_element(By.CLASS_NAME,'text-h4.ml-1.color-800').text
        except Exception :
            price = np.nan

    properties_list = f"{properties_list}"
    image = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/img').get_attribute('src')
    return pd.Series({'bio':bio, 'properties' : properties_list, 'price' : price, "image" : image})

def divar(driver) :
    """for products in divar market
    [bio] = bio of product
    [properties] = properties of product
    [template] = template that properties lie there
    [properties_list] = list of propertes texts"""

    bio = driver.find_element(By.CLASS_NAME,'kt-page-title__title.kt-page-title__title--responsive-sized').text
    template = driver.find_element(By.CLASS_NAME,'post-page__section--padded')
    properties = template.find_elements(By.CLASS_NAME,"kt-base-row.kt-base-row--large.kt-unexpandable-row")

    properties_list = []
    prices = []
    for properti in properties :
        string = properti.text.replace("\n",': ').replace("\u200c",'')

        if re.findall("قیمت",string) or re.findall('پرداخت',string) or re.findall('ودیعه', string) :
            prices.append(','.join(re.findall('[\d]+',string)))

        else :
            properties_list.append(string)


    if len(prices) == 0 :
        price = np.nan
    else :
        price = prices[0]


    properties_list = f"{properties_list}"

    try :
        image = driver.find_element(By.CLASS_NAME,'kt-image-block__image.kt-image-block__image--fading').get_attribute('src')
    except Exception :
        image = np.nan
    return pd.Series({'bio':bio, 'properties' : properties_list,'price' :price,'image' : image})

def tecnolife(driver) :
    """for products in tecnolife market
    [bio] = bio of product
    [properties] = properties of product
    [template] = template that properties lie there
    [properties_list] = list of propertes texts"""
    bio = driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div[3]/section[1]/header/div/h1/strong').text
    properties = driver.find_elements(By.CLASS_NAME,'order_summary_pdp')
    properties_list = []
    for properti in properties :
        properties_list.append(properti.text)

    properties_list = f"{properties_list}"

    price = driver.find_element(By.CLASS_NAME,'product_productPrice__1z46Z').find_element(By.CLASS_NAME,'product_sameTransition__ZxNeN').text

    image = driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div[3]/section[1]/div[2]/div[2]/div/img').get_attribute('src')

    return pd.Series({'bio' : bio, 'properties' : properties_list, 'price':price, 'image':image})


def helper() :
    """this module will give you the web page of product
    the main function is named 'main' to use it
    firstly give the products webpage link.
    secondly give what market does webpage belongs to ('digikala','tecnolife','divar')
    in the end you will receive a Series object :   
    pd.Series({'bio' : bio, 'properties' : properties_list, 'price':price, 'image':image})""" 

if __name__ == "__main__" :
    help(helper)
    print(main('https://www.technolife.ir/product-3763/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-15.6-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D9%84%D9%86%D9%88%D9%88-%D9%85%D8%AF%D9%84-ideapad-gaming-3-15ihu6-i5-8gb-512gb-11h','tecnolife'))