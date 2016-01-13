# -*- coding:utf-8 -*-
__author__ = 'ccyjava'

# bb[0]:股票名  bb[1]:今日开盘价    bb[2]：昨日收盘价    bb[3]:当前价格   bb[4]:今日最高价    bb[5]:今日最低价
# bb[6]:买一报价 bb[7]:卖一报价     bb[8]:成交股票数/100 bb[9]:成交金额/w bb[10]:买一申请股数 bb[11]:买一报价
# bb[12]:买二股数 bb[13]:买二报价   bb[14]:买三股数      bb[15]:买三报价  bb[16]:买四申请股数 bb[17]:买四报价
# bb[18]:买五股数 bb[19]:买五报价   bb[20]:卖一股数      bb[21]:卖一报价  bb[22]:卖二申请股数 bb[23]:卖二报价
# bb[24]:卖三股数 bb[25]:卖三报价   bb[26]:卖四股数      bb[27]:卖四报价  bb[28]:卖五股数     bb[29]:卖五报价
# bb[30]:日期     bb[31]:时间     bb[8]:不知道

import urllib2
import time
from stock_sort import stocksort
from data_center import *
import json
import datetime as dt


is_debug = True
data_center = StockDataCenter()



def print_dict(data):
    data_list = data
    if isinstance(data, dict):
        data_list = data.items()

    for k, v in data_list:
        print str(k) + "    " + str(v)





if __name__ == '__main__':


    count = 0


    for stock_id in data_center.stock_id_list:
        key = stock_id + "_" + data_center.stock_id_to_name[stock_id]
        data_center.stock_increase_rate[key] = []
        count += 1
        if count < 800:
            stock_id_string += stock_id + ","
        else:
            data_center.update_batch_stock_state(stock_id_string.strip(","))
            stock_id_string = ""
            count = 0
    data_center.update_batch_stock_state(stock_id_string.strip(","))

    print_dict(data_center.stock_increase_rate)
    while True:
        try:
            time.sleep(1)
            stock_id_string = ""
            count = 0
            for stock_id in data_center.stock_id_list:
                count += 1
                if count < 800:
                    stock_id_string += stock_id + ","
                else:
                    data_center.update_batch_stock_state(stock_id_string.strip(","))
                    stock_id_string = ""
                    count = 0
            data_center.update_batch_stock_state(stock_id_string.strip(","))

            # print stockDict
            xx = stocksort(data_center.stock_increase_rate)
            print "===========Top 10 ==========="
            print dt.datetime.now().time()
            print_dict(xx.getSort()[0:10])
        except:
            pass

