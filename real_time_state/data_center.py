# -*- coding:utf-8 -*-
__author__ = 'ccyjava'


import urllib2
import datetime as dt
import json


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
        self.stock_state={}
        self.stock_increase_rate={}
        self.stock_id_to_name={}

        file_of_stock_id_list = open("../stock_list.json", "r")
        self.stock_id_list = json.load(file_of_stock_id_list)
        # stock_name_map={}
        for item in self.stock_id_list:
            self.stock_id_to_name[item["stockCode"]] = item["stockName"].encode("utf-8")
        self.stock_id_list = map(lambda x: x.get('stockCode').encode("utf-8"), stock_id_list)
        file_of_stock_id_list.close()



    def get_batch_stock_state(self, stock_ids):
        ret_stock_state_list = {}
        contents = self._access_net(self.url + str(stock_ids))
        for content in str(contents).splitlines():
            stock_current_state = content.split(",")
            if len(stock_current_state) <= 2:
                continue
            try:
                s_id = str(stock_current_state[0][11:19]).encode("utf-8")
                s_name = self.stock_id_to_name[s_id]
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
                    self.stock_increase_rate[stock_key] = [stock_current_state_pro[stock_key][0]]
                self.stock_state[stock_key] = [stock_current_state_pro[stock_key][1]]
        except:
            print "error"


    def update_all_stock_state(self):
        pass