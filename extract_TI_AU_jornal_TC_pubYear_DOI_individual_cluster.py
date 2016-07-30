#!/usr/bin/python
# coding: utf-8
import os
import os.path
import urllib
import codecs
import glob
import re
from collections import OrderedDict

list_of_files = glob.glob("../../PRM_fulldata_close_analysis/*.txt")

#list_of_files = glob.glob("./*.txt")

matches2 = []
m=0
authors = re.compile(r'^AF\s')
title = re.compile(r'^TI\s')
journal = re.compile(r'^SO\s(.*)')
find_TC = re.compile(r'^TC\s(.*)')
PYear = re.compile(r'^PY\s(.*)')
reg2 = re.compile(r"^DI\s(.*)")
needed_title = str()
needed_paper = str()
au_list = str()
au_list_int = str()
title_list = str()
needed_title = str()
TC_interest = str()
PYear_interest = str()

list_paper_title = []

countAUi = 0
countTIi = 0
countJOi = 0
counta = 0
countb = 0
countc = 0

for fileName in list_of_files:
    fin = open(fileName, "r")
    data_list = fin.readlines()
    fin.close()
    for line2 in data_list:
            matchauthors = authors.findall(line2[:3])
            neededauthors = ' '.join(matchauthors)
#            print neededauthors
            countAUi += 1
            if neededauthors:
               counta = countAUi
#               print counta
            matchtitle = title.findall(line2[:3])
            neededtitle = ' '.join(matchtitle)
#            print neededtitle
            countTIi += 1
            au_list = str()
            if neededtitle:
               countb = countTIi
               for i in range(counta-1,countb-1):
                   au_list += (data_list[i][3:].strip() + ';')
               au_list_int = au_list 
#               print au_list.strip()       
            matchJO = journal.findall(line2)
            journal_name = ' '.join(matchJO)
            countJOi += 1
            title_list = str()
            if journal_name:
               countc = countJOi
               for j in range(countb-1,countc-1):
                   title_list += (data_list[j][3:].strip() + ' ')
               needed_title = title_list
            matchSO1 = journal.findall(line2)
            needed_journal = ' '.join(matchSO1) 
            if needed_journal:
               j_interest = needed_journal
            matchTC = find_TC.findall(line2)
            neededTC = ' '.join(matchTC)
            if neededTC:
               TC_interest = 'TC'+'='+str(neededTC)
               print TC_interest
            matchPYear = PYear.findall(line2)
            neededPYear = ' '.join(matchPYear)
            if neededPYear:
               PYear_interest = neededPYear
               print PYear_interest
            matches2 = reg2.findall(line2)
    	    if matches2:
               needed_paper = 'http://doi.org/' +  ' '.join(matches2).strip() + '  ' + needed_title + '  ' + au_list_int + '  ' + j_interest+ '  '+TC_interest + '  '+PYear_interest
               print needed_paper
               list_paper_title.append(needed_paper)
    countAUi = 0
    countTIi = 0
    countJOi = 0
    counta = 0
    countb = 0
    countc = 0

n_paper = len(list_paper_title)
for y in range(0,n_paper):
    print list_paper_title[y]

file1 = open("1Materials_journals_closed_network.tree", "r")
list1 = file1.readlines()

paper_cluster = []

for item in list1:
    line = item
    interest = line.split(' ')
#    paper_cluster.append(interest[0].strip())
    paper_cluster.append(interest[0].strip() + '  ' + interest[2].strip())

n_ppr_clust = len(paper_cluster)

#...................................

dir = '/Users/hari/Desktop/PR_Materials/PRM_fulldata_close_analysis/0Analyse/DOIS/'

pub_ID_int = str()

for x in range(0,n_paper):
    pub_ID = list_paper_title[x].split('  ')
    pub_ID_int = pub_ID[0][18:22].replace('/','')# replace fixes a wrong three digit DOI issue
    print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    print pub_ID_int
    filename_DOI = dir +  str(pub_ID_int)  
    output = open(filename_DOI, "w")
    output.close()

for nds2 in range(0,n_paper):
    pub_ID_1 = list_paper_title[nds2].split('  ')
    pub_ID_1_int = pub_ID_1[0][18:22].replace('.','O').replace('/','O').replace('  ','').replace('-','').replace('/','') 
    filename = dir + str(pub_ID_1_int)
    output_new = open(filename, "a")
    output_new.write(list_paper_title[nds2])
    output_new.write('\n')
    output.close()  

cluster_title = []

for n1 in range(0,n_ppr_clust):
    p_interest = paper_cluster[n1].split('  ')
    p_cluster = p_interest[1]
#    print p_interest[0] 
    for_doi = paper_cluster[n1].split('  ')
    doi = for_doi[1][19:23].replace('.','O').replace('/','O').replace('  ','').replace('-','').replace('/','')
#    print doi
    file_1 = dir + str(doi)
    if os.path.exists(file_1):
#       print 'file_found'
       input = open(file_1, 'r')
       read_papers = input.readlines()
       for lines in read_papers:
           matching_paper = str(lines.split('  ')[0].strip())
#           print matching_paper
           if str(matching_paper) == str(p_cluster[1:-1].strip()):
              print 'found_matching_paper'
              print (p_interest[0].strip() + '  ' + lines)
              cluster_title.append(p_interest[0].strip() + '  ' + lines)
              break

size_CT = len(cluster_title)

for n00 in range(1,101):
    cluster_ID = n00
    file_name = 'directed_materials_closed_links_cluster_TI_JN_TC_PY_AU_DOI_'+str(cluster_ID)+'.html'
    print file_name
    output = open(file_name, "w")
    output.write('<!DOCTYPE html>')
    output.write('\n')
    output.write('<html>')
    output.write('\n')
    output.write('<body>')
    output.write('\n')
    output.write('<pre>')
    for n3 in range(0,size_CT):
        paper_link = cluster_title[n3].split('  ')
        cluster_tree_ID = paper_link[0]
        top_cluster_ID = cluster_tree_ID.split(':')[0]
        if int(top_cluster_ID) == int(cluster_ID):
           print top_cluster_ID 
           output.write(paper_link[0] +'     '+'<a'+ ' ' + 'href=' + paper_link[1] + '>' + paper_link[2] + '</a>')
           output.write('<br>')
           output.write('DOI:' + paper_link[1][15:] + '  '+ 'JN:'+ paper_link[4] + '  ' + 'PY:' + paper_link[6] + '  '+ 'TC:'+ paper_link[5][3:] + '  ' + 'AU:'  + paper_link[3])
           output.write('<br>')
    output.write('</pre>')
    output.write('\n')
    output.write('</body>')
    output.write('</html>')
