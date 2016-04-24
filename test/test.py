#!/usr/bin/env python
# -*-coding:utf-8 -*-


import zoomeye.zoomeye as zoomeye

test = zoomeye.myeye()


test.search('web',query='dedecms',page=5,config=None)

test.search('host',query='port:21',page=5,config=None)