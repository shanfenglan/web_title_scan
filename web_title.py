#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/4 16:56
# @Author  : shanfenglan
# @File    : web_title.py
# @Software: PyCharm
import argparse,netaddr
import re,requests,threading,time,os
import sys

class wt():
    def __init__(self):
        self.out = []
        self.flag = 0
        self.url_list = list
        self.thread_list = []
        self.result = []
        self.lock = threading.Lock()
        self.semphore = threading.Semaphore(20)
    def run(self,listt):
        try:
            self.lock.acquire()
            self.pattern = '<title>(.*?)</title>'
            response = requests.get(listt,timeout=3).text
            title = re.findall(self.pattern, response)
            ccc = listt + '{**}'+title[0]
            self.result.append(ccc)
            print(ccc)
            self.lock.release()
        except:
            if 'https' in listt:
                print("\033[1;31;40m"+'[--]'+listt+'------>     https协议访问失败'+"\033[0m")
                pass
            else:
                print("\033[1;31;40m"+'[--]'+listt+'------>      http协议访问失败'+"\033[0m")
                pass
            self.lock.release()
    def generate_thread(self):
        for i in range(len(self.url_list)):
            thread = threading.Thread(target=self.run,kwargs={"listt":self.url_list[i]})
            self.thread_list.append(thread)

    def start_thread(self):
        for i in self.thread_list:
            self.semphore.acquire()
            i.start()
            self.semphore.release()

        for i in self.thread_list:
            i.join()

    def auto(self):
        self.generate_thread()
        self.start_thread()
    def fi(self):
        f = open(pwd2, 'w')
        for i in self.result:
            f.writelines(i + '\n')
        print('\n\n\033[1;32;40m[++]The result file was saved in'+pwd2+'\033[0m')

def parser_error(errmsg):
    print("Usage: python3 " + sys.argv[0] + " [Options] use -h for help. \n")
    errormessage = "Error: " + errmsg
    print("\033[1;36;40m" + errormessage + "\033[0m")
    sys.exit()


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -l 1.txt")
    parser.error = parser_error  # rewrite function
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-l', '--list', dest='list', nargs=1, help='ip list file,the content was supported CIDR')
    # parser.add_argument('-i', '--ip', dest='ip', nargs=1, help='ip list')
    return parser.parse_args()


if __name__ == '__main__':
    c = parse_args().list
    if c == None:
        print("Usage: python3 " + sys.argv[0] + " [Options] use -h for help. \n")
        sys.exit()


    # -------------------------#
    position = os.getcwd()
    b = ''
    for i in range(1, 6):
        a = str(time.localtime()[i]) + '_'
        b = b + a
    pwd = c[0]
    pwd2 = position + "/" + b + "result.txt"
    list = []
    name = []


    def manipulate(s):
        res = 'http://' + str(s)
        res1 = 'https://' + str(s)
        ress = [res, res1]
        return ress

    with open(pwd, 'r') as temporary_file:
        ipArray = []
        for i in temporary_file:
            try:
                if int(i.split('.')[0]) < 255:
                    i = i.strip("\n")
                    # i = manipulate(i)
                    list.append(i)
            except:
                pass
    # print(list)
    ipArray = []
    for i in list:  # data processing
        ipArray.extend([str(i) for i in netaddr.IPNetwork(i)])
    list = ipArray
    aaa = []
    for i in list:
        i = manipulate(i)
        aaa.extend(i)
    list = aaa
    # -------------------------#

    parse_args()
    test = wt()
    test.auto()
    test.fi()
