import pandas as pd
import numpy as np

def get(username):
    """a getter for the user favorites
    [username] = username of client
    [df] = df of all clients with their favorite product"""
    df = pd.read_csv("user_favorites.csv")
    df = df[df["username"] == username]

    if len(df) == 0 :
        return np.nan
    
    return df

def set(username ,image ,discrip ,price ,link ,market):
    """a setter for the user favorites
    [username] = username of client
    [df] = df of all clients with their favorite product"""
    username = username
    df = pd.read_csv('user_favorites.csv')
    df.set_index(['username','index'],inplace=True)
    try :
        df.loc[(username,len(df.loc[username])),:] = pd.Series({"discrip" : discrip,'price':price,'image':image,'link' : link,'market' : market})
    except KeyError :
        df.loc[(username,0),:] = pd.Series({"discrip" : discrip,'price':price,'image':image,'link' : link,'market' : market})
    df.to_csv('user_favorites.csv')

    return df.loc[username]


def delete(username,product_num) :
    """a deletter for user favorites
    [username] = username of client
    [product_num] = a pointer to the product we want to unfavorite it"""
    df = pd.read_csv("user_favorites.csv").set_index(["username",'index'])
    df.drop([(username,product_num)],axis='index',inplace=True)
    df.to_csv("user_favorites.csv")

    return df.loc[username]
def main(order,**kwargs) :
    if order == "set" :

        return set(kwargs['username'], kwargs['image'], kwargs['discrip'], kwargs['price'],kwargs['link'],kwargs['market'])

    elif order == 'get' :
        return get(kwargs['username'])

    elif order == 'del' :
        return delete(kwargs['username'],kwargs['product_index'])

def helper() :
    """this module is for saving the favorite products of client
    the main function is named 'main' for using this function
    you have to firstly define your order,your order must be 'set','get' or'del'
    you have give your arguments correctly to main function work so pay attention
    to the examples that we commented from line 63 to 66 so you get your desired\
    result."""

if __name__ == "__main__" :
    help(helper)
    #set("I-STALKER-I",'link\felan\besal\ssssssssis','lolddddolololol','0$','lidfssnk\felan\besal','meriikh')
    #print(main("set",username='I-STALKER-I',discrip = 'something', price = 12345,image = 'link\www\w\w\w\w\w',link = 'productpage_link',market = 'notmahdistore'))
    #print(main("get",username='I-STALKER-I'))
    #print(main('del',username='I-STALKER-I',product_index=3))
