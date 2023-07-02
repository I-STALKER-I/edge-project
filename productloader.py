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
        divar(driver)

    else :
        tecnolife(driver)

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


    properties_list = f"{properties_list}"
    print(properties_list)
    image = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/img').get_attribute('src')
    return pd.Series({'bio':bio, "image" : image, 'properties' : properties_list})

def divar(driver) :
    """for products in divar market"""
    template = driver.find_element(By.CLASS_NAME,'post-page__section--padded')
    properties = template.find_elements(By.CLASS_NAME,"kt-base-row.kt-base-row--large.kt-unexpandable-row")
    producst_list = []
    for properti in properties :
        print(repr(properti.text.replace("\n",': ').replace("\u200c",'')))

def tecnolife(driver) :
    """for products in tecnolife market"""
    pass

def helper() :
    """""" 

if __name__ == "__main__" :
    main('https://divar.ir/v/%DA%A9%D8%A7%D8%B1%D8%AA%D9%86-%D8%A7%D8%B3%D8%A8%D8%A7%D8%A8-%DA%A9%D8%B4%DB%8C-%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D8%A2%D8%B4%D9%BE%D8%B2%D8%AE%D8%A7%D9%86%D9%87-%D9%88%D8%A8%D8%B1%D9%82%DB%8C-_%D8%B9%D9%85%D8%AF%D9%87-%D9%81%D8%B1%D9%88%D8%B4%DB%8C_%D8%AA%D9%87%D8%B1%D8%A7%D9%86_%D9%85%DB%8C%D8%AF%D8%A7%D9%86-%D8%A7%D9%86%D9%82%D9%84%D8%A7%D8%A8_%D8%AF%DB%8C%D9%88%D8%A7%D8%B1/gYCdNDy0','divar')