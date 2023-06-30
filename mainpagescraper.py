import scraping
import multiprocessing

class gloablism :
    """a class for globalisation
    [table] = later dataframe for tablet scrapign
    [loptop] = later dataframe for loptop scrapign"
    [mobile] = later dataframe for mobile scrapign"
    [headphone] = later dataframe for headphone scrapign"
    [watch] = later dataframe for watch scrapign" """
    tablet = None
    loptop = None
    mobile = None
    headphone = None
    watch = None




def sender(queue,dicti) :
    """a func for sending multithreadly
    [queue] = queue for sending data
    [dicti] = the dictionary that is going to be sent"""
    queue.put(dicti)

def reciever(queue, kind) :
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
            dictionary = {'image':[scraping.np.nan],'discrip' : [scraping.np.nan],'price' : [scraping.np.nan], 'link' : [scraping.np.nan],'market' : [scraping.np.nan]}
            pass            

        else :
            dictionary[list(income.keys())[0]] = list(income.values())[0]

    if kind == "tablet" :
        gloablism.tablet = scraping.pd.DataFrame(dictionary)
        gloablism.tablet = gloablism.tablet.apply(kinding,args=(kind,),axis='rows')

    elif kind == "mobile" :
        gloablism.mobile = scraping.pd.DataFrame(dictionary)
        gloablism.mobile = gloablism.mobile.apply(kinding,args=(kind,),axis='columns')

    elif kind == 'headphone' :
        gloablism.headphone = scraping.pd.DataFrame(dictionary)
        gloablism.headphone = gloablism.headphone.apply(kinding,args=(kind,),axis='columns')

    elif kind == 'watch' :
        gloablism.watch =  scraping.pd.DataFrame(dictionary)
        gloablism.watch = gloablism.watch.apply(kinding,args=(kind,),axis='columns')
    
    else :
        gloablism.loptop = scraping.pd.DataFrame(dictionary)
        gloablism.loptop = gloablism.loptop.apply(kinding,args=(kind,),axis='columns')


def kinding(row,kind) :
    """in this function we want to put kind for each row for later multiindexing
    [row] = row of our dataframe
    [kind] = kind of row"""
    row["kind"] = kind
    return row


def sender(queue,dictionary) :
    """sender function
    [queue] = our connection with receiver
    [dictionary] = dictionary we want to send"""
    queue.put(dictionary)


def mobile(queue) :
    """mobile will be scraped in here
    [df] = dataframe for scraping
    [threader] = multithread sending from queue to receiver
    [queue] = our connection with receiver"""
    """mobile will be scraped in here"""
    df = scraping.multi_search('گوشی','1')
    #print(df.head(50))
    chunk_1 = df[df["market"] == "digikala"].head(4)
    chunk_2 = df[df["market"] == "tecnolife"].head(3)
    chunk_3 = df[df["market"] == 'divar'].head(3)
    df = scraping.pd.concat([chunk_1,chunk_2,chunk_3])
    threader(df,queue)
    queue.put('D')



def tablet(queue) :
    """tablet will be scraped in here
    [df] = dataframe for scraping
    [threader] = multithread sending from queue to receiver
    [queue] = our connection with receiver"""
    df = scraping.multi_search("تبلت",'1')
    chunk_1 = df[df["market"] == "digikala"].head(4)
    chunk_2 = df[df["market"] == "tecnolife"].head(3)
    chunk_3 = df[df["market"] == 'divar'].head(3)
    df = scraping.pd.concat([chunk_1,chunk_2,chunk_3])
    threader(df,queue)
    queue.put('D')



def loptop(queue) :
    """loptop will be scraped in here
    [df] = dataframe for scraping
    [threader] = multithread sending from queue to receiver
    [queue] = our connection with receiver"""
    df = scraping.multi_search('لپتاپ','1')
    chunk_1 = df[df["market"] == "digikala"].head(4)
    chunk_2 = df[df["market"] == "tecnolife"].head(3)
    chunk_3 = df[df["market"] == 'divar'].head(3)
    df = scraping.pd.concat([chunk_1,chunk_2,chunk_3])
    threader(df,queue)
    queue.put('D')

def headphone(queue) :
    """headphone will be scraped in here
    [df] = dataframe for scraping
    [threader] = multithread sending from queue to receiver
    [queue] = our connection with receiver"""
    df = scraping.multi_search('هدفون','1')
    chunk_1 = df[df["market"] == "digikala"].head(4)
    chunk_2 = df[df["market"] == "tecnolife"].head(3)
    chunk_3 = df[df["market"] == 'divar'].head(3)
    df = scraping.pd.concat([chunk_1,chunk_2,chunk_3])
    threader(df,queue)
    queue.put('D')


def watch(queue) :
    """watch will be scraped in here
    [df] = dataframe for scraping
    [threader] = multithread sending from queue to receiver
    [queue] = our connection with receiver"""
    df = scraping.multi_search('واچ','1')
    chunk_1 = df[df["market"] == "digikala"].head(4)
    chunk_2 = df[df["market"] == "tecnolife"].head(3)
    chunk_3 = df[df["market"] == 'divar'].head(3)
    df = scraping.pd.concat([chunk_1,chunk_2,chunk_3])
    threader(df,queue)
    queue.put('D')

def threader(df,queue) :
    df = df.reset_index()
    df_dict = df.to_dict()
    sender_threads = []

    #here we are sending data multithreadly
    for key, values in df_dict.items() :
        thread = scraping.threading.Thread(target=sender,args=(queue,{key:values}))
        thread.start()
        sender_threads.append(thread)

    for thread in sender_threads :
        thread.join()
    

def main() :
    """this is the main function
    [queue_1] = queue for tablet
    [queue_2] = queue for loptop
    [queue_3] = queue for headphone
    [queue_4] = queue for watch
    [queue_5] = queue for mobile
    [..._proc] = proccess of scraping for each search
    [..._receive] = to receive dictionaries being send from other side
    [global_df] = global dataframe that puts everything together"""
    queue_1 = multiprocessing.Queue()
    queue_2 = multiprocessing.Queue() 
    queue_3 = multiprocessing.Queue()
    queue_4 = multiprocessing.Queue()
    queue_5 = multiprocessing.Queue()
    tablet_proc = multiprocessing.Process(target=tablet,args=(queue_1,))
    loptop_proc = multiprocessing.Process(target=loptop,args=(queue_2,))
    headphone_proc = multiprocessing.Process(target=headphone,args=(queue_3,))
    watch_proc = multiprocessing.Process(target=watch,args=(queue_4,))
    mobile_proc = multiprocessing.Process(target=mobile,args=(queue_5,))

    tablet_receive = scraping.threading.Thread(target = reciever,args=(queue_1,'tablet'))
    loptop_receive = scraping.threading.Thread(target = reciever,args=(queue_2,'loptop'))
    headphone_receive = scraping.threading.Thread(target = reciever,args=(queue_3,'headphone'))
    watch_receive = scraping.threading.Thread(target = reciever,args=(queue_4,'watch'))
    mobile_receive = scraping.threading.Thread(target = reciever,args=(queue_5,'mobile'))

    tablet_proc.start()
    loptop_proc.start()

    tablet_receive.start()
    loptop_receive.start()

    tablet_receive.join()
    loptop_receive.join()


    headphone_proc.start()
    watch_proc.start()

    headphone_receive.start()
    watch_receive.start()

    headphone_receive.join()
    watch_receive.join()


    mobile_proc.start()    
    mobile_receive.start()
    mobile_receive.join()

    global_df = scraping.pd.concat([gloablism.headphone,gloablism.loptop,gloablism.mobile,gloablism.tablet,gloablism.watch])
    global_df = global_df.set_index(['kind','index'])


    return global_df.dropna()


def helper():
    """this is a receiver for main page of application
    note: this module may open many chromedriver be careful if your computer
    is not powerful the main function is named 'main' that runs without any arguments"""

if __name__ == "__main__":
    help(helper)
    print(main())





