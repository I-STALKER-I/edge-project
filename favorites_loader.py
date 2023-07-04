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
    print(df.set_index(['username','index'],inplace=True))
    try :
        df.loc[(username,len(df.loc[username])),:] = pd.Series({"discrip" : discrip,'price':price,'image':image,'link' : link,'market' : market})
    except KeyError :
        df.loc[(username,0),:] = pd.Series({"discrip" : discrip,'price':price,'image':image,'link' : link,'market' : market})

    print(df)
    df.to_csv('user_favorites.csv')


def delete(username,discrip) :
    pass

def main(order,row) :
    pass

def helper() :
    """this is the end """

if __name__ == "__main__" :
    help(helper)
    #set("I-STALKER-I",'link\felan\besal\ssssssssis','lolddddolololol','0$','lidfssnk\felan\besal','meriikh')
    print(get("I-STALKER-I"))