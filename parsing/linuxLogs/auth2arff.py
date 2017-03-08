#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import re
import codecs
from datetime import datetime
try:
    import arff
except ImportError:
    print "[ERROR] No arff library install. Please install with \"pip install arff\""
    quit()

debug = "yes"
log_year = "2017"

def parseFile(fileName):
    values_to_dump = []
    f = codecs.open(fileName,'r',"ISO-8859-1")
    lineCounter = 0
    for line in f:
    #{
        lineCounter = lineCounter + 1
        ## Search for section. Start new entry
        splitLine = line.split()
        tmp_month = splitLine[0]
        tmp_day = splitLine[1]
        tmp_time = splitLine[2]
        log_date = datetime.strptime(log_year+" "+tmp_month+" "+tmp_day+" "+tmp_time,"%Y %b %d %X")
        log_host = splitLine[3]
        service_match = re.search('(.*)\[([0-9]+)\]', splitLine[4])
        if service_match is None:
            print "Error getting service from line "+str(lineCounter)+" segment "+splitLine[4]
            continue
        log_service = service_match.group(1)
        log_service_pid = service_match.group(2)
        regExpMatch = re.search('\[ID ([0-9]+) (.*)\] (.*)', line)
        if regExpMatch is None:
            print "Error getting ID from line "+str(lineCounter)+" segment "+line
            continue
        log_ID = regExpMatch.group(1);
        log_type = regExpMatch.group(2);
        log_message = regExpMatch.group(3);

        ##Try to get a from IP
        regExpMatch = re.search('from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', log_message)
        log_ip = "?"
        if regExpMatch is not None:
            log_ip = regExpMatch.group(1)
        elif debug == "yes":
            print "[WARNING] No IP found on line: " + str(lineCounter) + " Message = " + log_message
        
        ##Analizing log_messages
        log_message_type = "?"
        ##Trying to get accept log_message
        log_accept_type = "?"
        log_user = "?"
        regExpMatch = re.search('Accepted (.*) for (\S+)', log_message) #\S matches any character which is not a Unicode whitespace character
        if regExpMatch is not None:
            log_message_type = "accepted"
            log_accept_type = regExpMatch.group(1)
            log_user = regExpMatch.group(2)
        elif debug == "yes":
            regExpMatch = re.search('Accept', log_message) #\S matches any character which is not a Unicode whitespace character
            if regExpMatch is not None:
                log_message_type = "accepted"
                print "[WARNING] Accept message I couldn't get all the info in line " + str(lineCounter) + " Message = " + log_message

        ##Trying to get Authorize
        regExpMatch = re.search('Authorized to (\S+),', log_message) #\S matches any character which is not a Unicode whitespace character
        if regExpMatch is not None:
            log_message_type = "authorized"
            log_user = regExpMatch.group(1)
        elif debug == "yes":
            regExpMatch = re.search('Authorized', log_message) #\S matches any character which is not a Unicode whitespace character
            if regExpMatch is not None:
                log_message_type = "authorized"
                print "[WARNING] Authorized Message with no user " + str(lineCounter) + " Message = " + log_message

        regExpMatch = re.search('refused', log_message) #\S matches any character which is not a Unicode whitespace character
        if regExpMatch is not None:
            log_message_type = "refused"

        ##If log_message not identified do not include it and print line info if debug
        if log_message_type == "?":
            if debug == "yes":
                print "[WARNING] Line " + str(lineCounter) + " contain no known message: " + log_message
        else:
            new_value = [str(log_date), log_host, log_service, log_service_pid, log_ID, log_type, log_message_type, log_accept_type, log_user, log_ip]
            values_to_dump.append(new_value)
    #}
    ## dump the log if there is anything
    if len(values_to_dump) != 0:
        arff.dump('auth.log.arff',values_to_dump,relation="authLogs",names=['date','host','service','service pid','ID','log type','messagetype','accept type', 'user', 'ip'])
    else:
        print "[info]Nothing to log"
            
parseFile("auth.log")
