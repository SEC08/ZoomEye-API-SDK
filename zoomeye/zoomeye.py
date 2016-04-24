#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import json
import sys
import time

class myeye(object):
    access_token = ''
    result = []
    hostresult = []
    webresult = []
    query = ''
    page = None
    config = None

    """docstring for myeye"""
    def __init__(self):
        super(myeye, self).__init__()

    # 输入用户米密码 进行登录操作
    # return: 访问口令 access_token
    def login(self):
        username = raw_input('[+] input : username:')
        password = raw_input('[+] input : password:')
        data = {
            'username' : username,
            'password' : password
        }
        data_encoded = json.dumps(data)  # dumps 将 python 对象转换成 json 字符串
        try:
            resp = requests.post(url = 'http://api.zoomeye.org/user/login',data = data_encoded)
            resp_decode = json.loads(resp.content) # loads() 将 json 字符串转换成 python 对象
            global access_token
            access_token = resp_decode['access_token']
        except Exception,e:
            print '[-] info : username or password is invalid, please try again '
            exit()


    # 将字符串写如文件中,方便下次登录
    def saveTokenToFile(self, file, token):
        with open(file,'wb') as output:
            output.write(token)
        if os.path.isfile('token.tmp'):
            print '[+] Token file saved!'


    #将搜索结果写入文件
    def saveResultToFile(self, file, result):
        result_name = ''

        if os.path.isfile(file):
            file = file.split('.')
            file_name = file[0]
            file_ext = file[1]

            current_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(time.time()))
            file_name += str(current_time)
            result_name = file_name + '.' + file_ext
        else:
            result_name = file

        s = '\n'.join(result)

        with open(result_name,'w') as output:
            output.write(s)

        if os.path.isfile(result_name):
            print '[+] Search result has saved!'


    #获取token
    def getToken(self):
        global access_token
        if not os.path.isfile('token.tmp'):
            print '[-] info : access_token file is not exist, please login'
            self.login()
            # self.saveTokenToFile('token.tmp',access_token)
        else:
            with open('token.tmp','rb') as token:
                access_token = token.read()
            self.checkLogIn()

        self.saveTokenToFile('token.tmp',access_token) #执行完成以后把token更新
        return access_token



    #通过获取用户信息来验证token的有效性
    def checkLogIn(self):
        global access_token
        headers = {
            'Authorization' : 'JWT ' + access_token,
        }

        try:
            resp = requests.get(url='http://api.zoomeye.org/resources-info',headers=headers)
            resp_content = json.loads(resp.content)
            if resp_content['error'] == 'unauthorized':
                print 'Unauthorized, please login'
                self.login()
        except Exception, e:
            pass


    #获取用户信息
    def getInfo(self):
        try:
            global access_token
            headers = {
                'Authorization' : 'JWT ' + access_token,
            }
            resp = requests.get(url='http://api.zoomeye.org/resources-info',headers=headers)

            try:
                host_search = json.loads(resp.content)['resources']['host-search']
                web_search = json.loads(resp.content)['resources']['web-search']
                return  host_search,web_search
            except Exception, e:
                print 'Unauthorized, please login'
                self.login()
        except Exception, e:
            raise e


    #host搜索函数
    #query(string)指定搜索内容，page(int)为搜索页数，config(list)控制输出数据，默认全部输出
    def hostSearch(self,query='port:23',page=1,config=None):
        self.getToken()
        search_page = 1
        global hostresult
        global access_token

        #获取用户可以搜索的最大量
        host_search_top_num = int(self.getInfo()[0])

        if (page * 10) >= host_search_top_num:
            print '[-] info : account was break, excceeding the max limitations'
            sys.exit()

        # 将 token 格式化并添加到 HTTP Header 中
        headers = {
            'Authorization' : 'JWT ' + access_token,
        }
        # print headers
        while(True):
            try:
                resp = requests.get(url = 'http://api.zoomeye.org/host/search?query=%s&facet=app,os&page=%d' % (str(query),int(search_page)),headers = headers)
                resp_decode = json.loads(resp.content)

                for x in resp_decode['matches']:
                    print x['ip']
                    self.hostresult.append(x['ip'] + '\n')
                print '[-] info : count ' + str(search_page * 10)
                print '-----------------------------------'

            except Exception,e:
                # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
                if str(e.message) == 'matches':
                    print '[-] info : account was break, excceeding the max limitations'
                    break
                else:
                    print  '[-] info : ' + str(e.message)
            else:
                if search_page >= page:
                    break
                search_page += 1



    #web搜索函数
    #query(string)指定搜索内容，page(int)为搜索页数，config(list)控制输出数据，默认全部输出
    def webSearch(self,query='dedecms',page=1,config=None):
        self.getToken()
        search_page = 1
        global webresult
        global access_token

        #获取用户可以搜索的最大量
        web_search_top_num = int(self.getInfo()[1])

        if (page * 10) >= web_search_top_num:
            print '[-] info : account was break, excceeding the max limitations'
            sys.exit()

        # 将 token 格式化并添加到 HTTP Header 中
        headers = {
            'Authorization' : 'JWT ' + access_token,
        }
        # print headers
        while(True):
            try:
                resp = requests.get(url = 'http://api.zoomeye.org/host/search?query=%s&facet=app,os&page=%d' % (str(query),int(search_page)),headers = headers)
                resp_decode = json.loads(resp.content)

                for x in resp_decode['matches']:
                    print x['ip']
                    self.webresult.append(x['ip'] + '\n')
                print '[-] info : count ' + str(search_page * 10)
                print '-----------------------------------'

            except Exception,e:
                # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
                if str(e.message) == 'matches':
                    print '[-] info : account was break, excceeding the max limitations'
                    break
                else:
                    print  '[-] info : ' + str(e.message)
            else:
                if search_page >= page:
                    break
                search_page += 1


    #搜索函数
    def search(self, search_type='web', query='dedecms', page=1, config=None):
        global result
        global webresult
        global hostresult

        if search_type == 'web':
            self.webSearch(query, page, config=None)
            self.result = self.webresult
        elif search_type == 'host':
            self.hostSearch(query, page, config=None)
            self.result = self.hostresult
        else:
            print 'error! params is invalid'

        self.saveResultToFile('result.txt',self.result)

        return

