#coding:utf-8 
import urllib2,urllib
import sys
import re
import cookielib
import time
import sqlite3
from datetime import date

numofpage = 5

def login(i):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                'Referer' : '******','Connection':'keep-alive'}
    
    url='http://m.newsmth.net/board/Intern?p='+str(i);
    postdata={'id':'cool15684','passwd':'6090960','save':'on'}

    cj=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)


    postdata = urllib.urlencode(postdata)
    request = urllib2.Request(url=url,data=postdata,headers = headers)

    respose = urllib2.urlopen(request)


    text = respose.read()

    type = sys.getfilesystemencoding()
     #txt = txt.decode('gbk').encode(type)
    f = open('job'+str(i)+'.html','w')
    f.write(text)
    f.close()

if __name__ == '__main__':
    idjob= open('joblastid.txt','r')
    jobid_str = idjob.read()    
    joblastid_int = int(jobid_str)
    idjob.close()
    temp_id =joblastid_int

    
    for i in xrange(1,numofpage+1):
        login(i);
    
    conn = sqlite3.connect('C:/Users/Administrator/Desktop/crawl/test.db')
    curs = conn.cursor()
    curs.execute('''CREATE TABLE if not exists job_shuimu( 
    id         INTEGER           PRIMARY KEY ASC AUTOINCREMENT,
    post_url   VARCHAR( 0, 30 ),
    post_title VARCHAR( 0, 60 ),
    post_time  DATE )''')


    for i in xrange(1,numofpage+1):
        job = open('job'+str(i)+'.html','r')
        begin = 0        
        jobread = job.read()
        job.close()
        
        cursor_id = jobread.find("/article/Intern/",begin,len(jobread))
        while(cursor_id>0):
            
            cursor_id_end = jobread.find("\"",cursor_id,len(jobread))

            post_id = jobread[cursor_id+16:cursor_id_end]
            
            
            cursor_title_begin = jobread.find(">",cursor_id_end,len(jobread))
            cursor_title_end = jobread.find("</a>",cursor_id_end,len(jobread))

            post_title = jobread[cursor_title_begin+1:cursor_title_end]


            cursor_time_begin = jobread.find("<div>",cursor_title_end,len(jobread))
            cursor_time_end  =  jobread.find("&",cursor_time_begin,len(jobread))

            post_time = jobread[cursor_time_begin+5:cursor_time_end]

            if(len(post_time)==8):
                now = date.today()
                post_time = now.isoformat()

            

            post_url="http://www.newsmth.net/nForum/#!article/Intern/"+post_id
            
            #post_title_utf=post_title.decode('utf-8').encode('utf-8')
            
            #curs.execute("insert into job_haha values(NULL,'%s','%s','%s')" %(post_url,post_title_utf,post_time))
            
            #print post_id
            #print post_title
            #print post_time

            
            
            if(int(post_id)>joblastid_int):
                curs.execute("insert into job_shuimu values(NULL,'%s','%s','%s')" %(post_url,post_title,post_time))

                if(temp_id<int(post_id)):
                    temp_id = int(post_id)
            
            
            cursor_id = jobread.find("/article/Intern/",cursor_title_end,len(jobread))
            
        
        conn.commit()
        


    idjob= open('joblastid.txt','w')   
    idjob.write(str(temp_id))
    idjob.close()


    curs.close()
    conn.close()
    



    


