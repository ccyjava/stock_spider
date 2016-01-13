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
from stockSort import stocksort
import json
import datetime as dt

stock_increase_rate = {}
stock_state = {}

stock_id_to_name = {}
stock_file = {}

is_debug = True


def check_time(time_now):
    time_0930 = dt.time(9, 30, 0)
    time_1130 = dt.time(11, 30, 0)
    time_1300 = dt.time(13, 0, 0)
    time_1500 = dt.time(15, 0, 0)

    if time_now >= time_0930 and time_now <= time_1130:
        return True

    if time_now >= time_1300 and time_now <= time_1500:
        return True
    return False

class DataOcean:
    def __init__(self):
        pass

    def save_data(self,key,value,time_now):
        fw = open("state_file/" + key + ".txt", "a")
        fw.write(key + "," + value + "\n")
        fw.close()
        print time_now
        print "Record stock " + key


class DebugHelper:
    def __init__(self):
        self.is_dubug = True

    def get_log_func(self):
        def tmp_func(msg):
            self.log(msg)

        return tmp_func

    def static_log_fun(cls):
        tmp_instance = cls()
        return tmp_instance.get_log_func()

    def log(self, msg):
        if self.is_debug:
            print msg


class StockDataCenter(object):
    def __init__(self):
        self.url = 'http://hq.sinajs.cn/list='
        self.data_ocean=DataOcean()

    def get_batch_stock_state(self, stock_ids):
        ret_stock_state_list = {}
        contents = self._access_net(self.url + str(stock_ids))
        for content in str(contents).splitlines():
            stock_current_state = content.split(",")
            if len(stock_current_state) <= 2:
                continue
            try:
                s_id = str(stock_current_state[0][11:19]).encode("utf-8")
                s_name = stock_id_to_name[s_id]
                key = s_id + "_" + s_name
                if float(stock_current_state[1]) != 0:
                    increase_rate = str((float(stock_current_state[3]) - float(stock_current_state[2])) / float(
                        stock_current_state[1]) * 100)
                    ret_stock_state_list[key] = [increase_rate, stock_current_state[31]]
                else:
                    ret_stock_state_list[key] = [0, stock_current_state[31]]
                time_now = dt.datetime.now().time()
                if check_time(time_now):
                    self.data_ocean.save_data(key,content,time_now)
                else:
                    print time_now
                    print "Not in deal time!"
            except:
                print "error in " + key
        return ret_stock_state_list

    @staticmethod
    def _access_net(url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        contents = response.read()
        contents = contents.decode("gbk").encode("utf-8")
        # print contents
        return contents

    def update_batch_stock_state(self, stock_ids):
        try:
            stock_current_state_pro = self.get_batch_stock_state(stock_ids)
            if len(stock_current_state_pro) > 0:
                for stock_key in stock_current_state_pro:
                    stock_increase_rate[stock_key] = [stock_current_state_pro[stock_key][0]]
                stock_state[stock_key] = [stock_current_state_pro[stock_key][1]]
        except:
            print "error"


def print_dict(data):
    data_list = data
    if isinstance(data, dict):
        data_list = data.items()

    for k, v in data_list:
        print str(k) + "    " + str(v)


if __name__ == '__main__':

    data_center = StockDataCenter()

    file_of_stock_id_list = open("../stock_list.json", "r")

    stock_id_string = ""
    count = 0
    stock_id_list = json.load(file_of_stock_id_list)
    # stock_name_map={}
    for item in stock_id_list:
        stock_id_to_name[item["stockCode"]] = item["stockName"].encode("utf-8")

    stock_id_list = map(lambda x: x.get('stockCode').encode("utf-8"), stock_id_list)
    file_of_stock_id_list.close()

    for stock_id in stock_id_list:
        key = stock_id + "_" + stock_id_to_name[stock_id]
        stock_increase_rate[key] = []
        # stock_file[key]=open("state_file/"+key+".txt","a")
        count += 1
        if count < 800:
            stock_id_string += stock_id + ","
        else:
            data_center.update_batch_stock_state(stock_id_string.strip(","))
            stock_id_string = ""
            count = 0
    data_center.update_batch_stock_state(stock_id_string.strip(","))

    print_dict(stock_increase_rate)
    while True:
        try:
            time.sleep(1)
            stock_id_string = ""
            count = 0
            for stock_id in stock_id_list:
                count += 1
                if count < 800:
                    stock_id_string += stock_id + ","
                else:
                    data_center.update_batch_stock_state(stock_id_string.strip(","))
                    stock_id_string = ""
                    count = 0
            data_center.update_batch_stock_state(stock_id_string.strip(","))

            # print stockDict
            xx = stocksort(stock_increase_rate)
            print "===========Top 10 ==========="
            print dt.datetime.now().time()
            print_dict(xx.getSort()[0:10])
        except:
            pass

