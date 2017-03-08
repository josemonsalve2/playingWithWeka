#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import re
import codecs


def parseFile(fileName):
    f = codecs.open(fileName,'r',"ISO-8859-1")
    for line in f:
        ## Search for section. Start new entry
        splitLine = line.split()
	month = splitLine[0]
	day = splitLine[1]
	time = splitLine[2]
	host = splitLine[3]
	service_aux = splitLine[4]
        service=service_aux.split("[")[0]
	ID = splitLine[6]
	status = splitLine[8]
	print month+" "+day+" "+time+" "+","+host+""

     	

parseFile("auth.log")
