# -*- coding:utf-8 -*-
__author__ = 'ccyjava'


import datetime as dt

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