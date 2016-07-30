#!/usr/bin/python
# coding: utf-8
import os
import os.path
import urllib
import codecs
import glob
import re
from collections import OrderedDict

list_of_files = glob.glob("./*.html")

#list_of_files = glob.glob("./*.txt")

Keyword1 = raw_input("keyword1: ")
print ('keyword1:'+ Keyword1) 

Keyword2 = raw_input("keyword2: ")
print ('keyword2:'+ Keyword2)

#Keyword3 = raw_input("keyword3: ")
#print ('keyword3:'+ Keyword3)


search_word1 = re.compile(Keyword1)
search_word2 = re.compile(Keyword2)

countw = 0

for fileName in list_of_files:
    fin = open(fileName, "r")
    data_list = fin.readlines()
    fin.close()
    for line1 in data_list:
            matchsearch_word1 = search_word1.findall(line1)
            word1 = ' '.join(matchsearch_word1)
            matchsearch_word2 = search_word2.findall(line1)
            word2 = ' '.join(matchsearch_word2)
            if word1 or word2:
               countw += 1
    print (fileName + '    ' + Keyword1 + '    '+ Keyword2 + '    ' + str(countw))
    countw = 0
