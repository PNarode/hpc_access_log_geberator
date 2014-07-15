#! /usr/bin/python

from __future__ import division
from multiprocessing import Process
import os
import random
import binascii
import sys
import argparse
import string
import time
import gzip


log_format_ver=2
request_id=""
cp_name=["apis.google","newmediarock","api.junior","pywork","ssl.gstatic","medialive","hutchison-whampoa","newtvlivess","techcrunch","sector-live"]
copass_origin=["174.16.201.4","178.235.60.72","180.172.255.40","98.255.65.255","204.34.6.0","25.54.67.83","172.168.191.0","233.34.52.7","132.67.2.1","80.34.123.65"]
copass_cdn_prefix=["cdn.orange.com", "cdn.kt.ac.in", "cdn.francetel.com", "cdn.newrocks.org","cdn.rapidn.in","cdn.coolstage.com","cdn.ntr.co.in","cdn.newforms.com","cdn.assel.com","cdn.apple.in"]
http_host=["www.google.com","www.youtube.com","corp.india.lapslogin.com","docs.python.org","www.gmail.com","newbuzz.co.in","www.rediffmail.com","live-os-mss.orangetv.orange.es","www.yahoo.com","corp-greenlive.es"]
copass_node=["node1","node2","node3","node4","node5"]
my_zone=400
remote_addr=""
msec=""
request_time=""
response_start_time=0
request_method=['GET','PUT']
request_url=""
http_ver=["HTTP/1.0","HTTP/1.1"]
status=200
sent_http_content_length=0
body_bytes_sent=0
cache_hit_bytes=0
bytes_sent=0
http_range=['bytes:0-499','bytes:500-999','bytes:1000-4999','5000-9999']
request_length=0
http_referer="-"
http_user_agent=""
sent_http_content_type=["video/mp4","audio/mp3","text/plain"]
http_accept_encoding="identity"
sent_http_content_encoding="-"
hpc_redirect_type=0
levels=[97600,800000,2800000,4000000,5000000]



def get_mss_url(n):
    address="http://%s" % http_host[n]
    n=random.randrange(7,10)
    for k in range(0,n):
        url=""
        c=random.randrange(1,3)
        if c==1:
            l=random.randrange(7,25)
            url=url.join(random.choice(string.hexdigits) for x in range(0,l))
        elif c==2:
            l=random.randrange(7,25)
            url=url.join(random.choice(string.digits) for x in range(0,l))
        else:
            l=random.randrange(7,25)
            url=url.join(random.choice(string.letters) for x in range(0,l))
        address=address+"/"+url
    return address



def split_time(entries,span):
    increment=[]
    total=0.0
    inc=(span*1000)/entries
    inc=(inc*2)+2
    block=entries/inc
    remain=entries%inc
    for i in range(0,inc):
        increment.append(block)
        total=total+(block*(i*0.001))
    diff=int((float(span)-total)*1000)
    if diff>0:
        if block==0:
            increment[0]=increment[0]-diff
            increment[1]=increment[1]+diff
        else:
            diff=diff+(remain*1000)
            increment[0]=increment[0]-diff
            increment[1]=increment[1]+diff
    else:
        diff=(0-diff)/(inc-1)
        for i in range(1,inc):
            q=diff/i
            r=diff%i
            increment[0]=increment[0]+q
            increment[i]=increment[i]-q
            increment[0]=increment[0]+1
            increment[r]=increment[r]-1
    return increment



def log_write(filename,rec,ctime,increment,compress):
    record=""
    if compress:
        fp=gzip.open(filename,"w")
        fp.close()
        fp=gzip.open(filename,"a")
    else:
        fp=file(filename,"w")
        fp.close()
        fp=file(filename,"a")
    i=0
    while i<rec:
        request_id="%00000d690034992762835%0000d00000000%0000d" % (random.randrange(00000,99999),random.randrange(0000,9999),random.randrange(0000,9999),)
        remote_addr="%d.%d.%d.%d" % (random.randrange(70,200),random.randrange(0,255),random.randrange(0,255),random.randrange(0,255),)
        ctime=float(ctime)+increment
        msec="%.3f" % ctime
        request_time="%d.%000d" % (random.randrange(0,1),random.randrange(000,999),)
        n=random.randrange(0,9)
        request_url=get_mss_url(n)
        j=random.randrange(0,1)
        if  j==1:
            request_url=request_url+'/QualityLevels(%d)/FragmentInfo(video=%d)' % (levels[random.randrange(0,4)],random.randrange(945700000,945799999),)
            body_bytes_sent=random.randrange(30000,999999)
            bytes_sent=random.randrange(20000,body_bytes_sent)
            cache_hit_bytes=random.randrange(10000,bytes_sent)
        elif j==2:
            request_url=request_url+'/QualityLevels(%d)/FragmentInfo(video=%d)' % (levels[random.randrange(0,4)],random.randrange(945700000,945799999),)
            body_bytes_sent=random.randrange(300,1000)
            bytes_sent=random.randrange(200,body_bytes_sent+1)
            cache_hit_bytes=random.randrange(100,bytes_sent+1)
        else:
            request_url=request_url+'/QualityLevels(%d)/FragmentInfo(video=%d)' % (levels[random.randrange(0,4)],random.randrange(945700000,945799999),)
            body_bytes_sent=random.randrange(300,1000)
            bytes_sent=random.randrange(200,body_bytes_sent+1)
            cache_hit_bytes=random.randrange(100,bytes_sent+1)
        http_user_agent="".join(random.choice(string.ascii_lowercase) for x in range(0,random.randrange(6,10)))
        http_user_agent=http_user_agent+"/1.%d" % random.randrange(1,10)
        hpc_redirect_type=random.randrange(0,5)
        request_length=len(request_url)
        if i>0:
            record=record+'\n'
        record=record+'%d %s %s %s %s %s %s %d %s %s %s %d %s %s %s %d %d %d %d %d %s %d "%s" "%s" "%s" "%s" "%s" %d' % (log_format_ver,request_id,cp_name[n],copass_origin[n],copass_cdn_prefix[n],http_host[n],copass_node[random.randrange(0,4)],my_zone,remote_addr,msec,request_time,response_start_time,request_method[random.randrange(0,1)],request_url,http_ver[random.randrange(0,1)],status,sent_http_content_length,body_bytes_sent,cache_hit_bytes,bytes_sent,http_range[random.randrange(0,3)],request_length,http_referer,http_user_agent,sent_http_content_type[j],http_accept_encoding,sent_http_content_encoding,hpc_redirect_type)
        if i%1000==0:
            fp.write(record)
            record=""
        i=i+1
    fp.write(record)
    record=""
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="It takes 5 command line arguments -b (Basename) -n (No of Records) -c (No of files generated) -s (Time Span in Seconds) -t (Start time in Epoch Seconds)")
    parser.add_argument("-b",required = True,action = "store",dest = "BASE_NAME",help = "Basename of output files")
    parser.add_argument("-n",required = True,action = "store",dest = "NUM_OF_RECORDS_PER_FILE",help = "number of log entries to be generated in each file",type=int)
    parser.add_argument("-c",required = True,action = "store",dest = "TOTAL_NUM_OF_FILES",help = "number of output file",type=int)
    parser.add_argument("-s",required = True,action = "store",dest = "TIME_SPAN_IN_SECONDS",help = "Span of Time for record generation",type=int)
    parser.add_argument("-t",required = False,action = "store",dest = "START_TIME_IN_EPOCH_SECONDS",help = "the start time in seconds (epoch time formate (Unix Timestamp))",type=int)
    parser.add_argument("-z",required = False,action = "store",dest = "COMPRESSION_NEEDED_OR_NOT",help = "Value in Boolean(True/False) indicating Compression required or not")
    result = parser.parse_args(sys.argv[1:])
    base = result.BASE_NAME
    entries= result.NUM_OF_RECORDS_PER_FILE
    count=result.TOTAL_NUM_OF_FILES
    span=result.TIME_SPAN_IN_SECONDS
    increment=span/entries
    try:
        ctime="%d.000" % result.START_TIME_IN_EPOCH_SECONDS
    except:
        ctime="%.3f" % time.time()
    p=[]
    start_time=time.time()
    try:
        print result.COMPRESSION_NEEDED_OR_NOT
        if result.COMPRESSION_NEEDED_OR_NOT=="True" or result.COMPRESSION_NEEDED_OR_NOT=="true":
            for i in range(1,count+1):
                filename=str(str(base)+"_"+str(i))+".gz"
                p.append(Process(target=log_write,args=(filename,entries,float(ctime),increment,True),))
        else:
            for i in range(1,count+1):
                filename=str(str(base)+"_"+str(i))
                p.append(Process(target=log_write,args=(filename,entries,float(ctime),increment,False)))
    except:
        for i in range(1,count+1):
            filename=str(str(base)+"_"+str(i))
            p.append(Process(target=log_write,args=(filename,entries,float(ctime),increment,False)))        
    for i in range(0,count):
        p[i].start()
    end_time=time.time()
    print "The time taken=%.2f min" % ((end_time-start_time)/60)
