import mysql.connector
from datetime import datetime , timedelta
import socket
import time
import logging
conn=mysql.connector.connect(user='root',password='666666',database='easymonitor',port=3308)
logging.basicConfig(level=logging.INFO , filename='myblog.log')
print('ready')

now= datetime.now()

nowstamp = now.timestamp()
datadict={'海峡支行':'','崇宁路支行':''}
for i in datadict:
        datadict[i]=nowstamp-4000
cury=conn.cursor()
curyval = cury.execute('select * from tab_alarmdata')
dbl =len( cury.fetchall() )
cury.close()


def dbtext():
        
        cur=conn.cursor()
        abb= cur.execute('flush tables')
        ab= cur.execute('select * from tab_alarmdata')

        values=cur.fetchall()
        
        vl=len(values)
        
        global dbl
        def text(x,y):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('21.202.201.77',5000))
                datalength=11+len(y)*2+len(str(x))
                rawdata='0'+str(datalength)+ '13665161652' + y + str(x) 
                data=rawdata.encode('gbk')
                s.send(data)
                print('send ok')
                print(s.recv(1024).decode('gbk'))

                s.close()

          
        
        
              
        for i in range(dbl-2,vl):
                                   
                datadate=datetime.strptime(values[i][9], '%Y-%m-%d %H:%M:%S')
                datenum=datadate.timestamp()
                bankname=values[i][2]
                if bankname in datadict:
                        
                        if datenum - datadict[bankname]>3600:
                                datadict[bankname]=datenum
                                logging.info(datadict)
                                text(values[i][7],values[i][2])
                else:
                        text(values[i][7],values[i][2])
                        datadict[bankname] = datenum
                        logging.info(datadict)
                

        logging.info(str(vl)+'times')    
        cur.close()
def dtt(inc=60):
        while True:
                dbtext()
                time.sleep(inc)
if __name__=='__main__':
        try:
                dtt(50)
        except Exception as e:
                logging.info(e)
conn.close()




