#! /usr/bin/env python3
#coding: utf-8

import os

# print(os.system('scrapy runspider data_scrapy.py -o characters.json'))

# os.system('rm -f doviz.json')
# os.system('scrapy runspider doviz.py -o doviz.json')
os.system("scrapy runspider -t json doviz.py -o - > doviz.json")
