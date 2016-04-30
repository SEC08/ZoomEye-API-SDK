#!/usr/bin/env python
# -*-coding:utf-8 -*-


import sys
import requests
import zoomeye.zoomeye as zoomeye

test = zoomeye.zoomeye()

username = 'your mail@qq.com'
password = 'your ZoomEye account passwod'

token = test.logIn(username, password)

result = test.search('web',query='HP Color LaserJet',page=1,facets='app,os')

print result

target = []

for i in result:
    for x in i['matches']:
        print x['ip']
        target.append(x['ip'][0])

print target
