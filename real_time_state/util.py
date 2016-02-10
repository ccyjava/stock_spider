# -*- coding:utf-8 -*-
__author__ = 'ccyjava'



import datetime as dt
from pymongo import MongoClient

def check_time(time_now):
    time_0930 = dt.time(9, 30, 0)
    time_1130 = dt.time(11, 30, 0)
    time_1300 = dt.time(13, 0, 0)
    time_1500 = dt.time(23, 59, 59)

    if time_now >= time_0930 and time_now <= time_1130:
        return True

    if time_now >= time_1300 and time_now <= time_1500:
        return True
    return False



class DataOcean: # save data
    def __init__(self):

        client = MongoClient()
        self.db = client.stock
        self.store_set=set()


    def process(self,key,stock_string):
        stock_element = {}
        stock_status={}
        values=stock_string.split(",")
        if len(values)<2:
            return None
        stock_element["name"]=key
        stock_element["price"]=values[3]
        stock_element["high_price"]=values[4]
        stock_element["low_price"]=values[5]
        stock_element["date"]=values[30]
        stock_element["time"]=values[31]

        stock_status["name"]=key
        stock_status["previous_open"]=values[1]
        stock_status["previous_close"]=values[2]
        return stock_element,stock_status


    def save_data(self,key,value,time_now):
        #store to filesystem
        if value:
            fw = open("state_file/" + key + ".txt", "a")
            fw.write(key + "," + value + "\n")
            fw.close()
        # store to mongodb
        stock_element,stock_status=self.process(key,value)
        if stock_element:
            collection_price=self.db.price
            collection_price.insert_one(stock_element)
        if stock_status and key not in self.store_set:
            collection_stock_status=self.db.stock_status
            collection_stock_status.insert_one(stock_status)
            self.store_set.add(key)
        #print time_now
        #print "Record stock " + key

