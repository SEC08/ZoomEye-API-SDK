#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import sys


class zoomeye(object):
    """docstring for zoomeye"""

    def __init__(self):
        self.access_token = ''
        self.search_type = ''
        self.query = ''
        self.page = 1
        self.facets = ''
        self.result = []

    def logIn(self, username, password):
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
            return access_token
        except Exception,e:
            print '[-] info : username or password is invalid, please try again '
            sys.exit()

    def getInfo(self):
        global access_token
        try:
            headers = {
                'Authorization' : 'JWT ' + access_token,
            }
            resp = requests.get(url='http://api.zoomeye.org/resources-info',headers=headers)

            try:
                user_type = json.loads(resp.content)['plan']
                host_search = json.loads(resp.content)['resources']['host-search']
                web_search = json.loads(resp.content)['resources']['web-search']
                info = 'Your account is %s, host search is %d and web search is %d' % (user_type,host_search,web_search)
                return info
            except Exception, e:
                print 'Unauthorized, please login'
        except Exception, e:
            raise e

    def search(self, search_type='web', query='dedecms', page=1, facets='app,os'):
        search_page = 1
        global access_token
        if search_type != 'web' and search_type != 'host':
            print 'error! params is invalid'

        # 将 token 格式化并添加到 HTTP Header 中
        headers = {
            'Authorization' : 'JWT ' + access_token,
        }

        while(True):
            try:
                resp = requests.get(url = 'http://api.zoomeye.org/%s/search?query=%s&facet=%s&page=%d' % (str(search_type),str(query),str(facets),int(search_page)),headers = headers)
                resp_decode = json.loads(resp.content)
                self.result.append(resp_decode)
            except Exception,e:
                # 若搜索请求超过 API 允许的最大条目限制 或者 全部搜索结束，则终止请求
                if str(e.message) == 'matches':
                    print '[-] info : account was break, excceeding the max limitations'
                    break
                else:
                    print  '[-] info : ' + str(e.message)
                    sys.exit()
            else:
                if search_page >= page:
                    break
                search_page += 1

        return self.result

