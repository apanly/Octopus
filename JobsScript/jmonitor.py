#!/usr/bin/python
#coding:utf-8

import sys,time,logging
from mysqlResource import mysqlOpe
from jqueuecons import __sql_alert_insert
from jqueuecons import getLocalDate

__sql_notrun="SELECT id,name,job_first_start,error_group,error_code FROM alertjoblist WHERE run_status=1 and  job_first_start<%d "
__alert_notrun_content="您的JOB(job_%s %s)应该在%s运行,但是现在还没有运行"

__sql_timeout="SELECT id,name,job_first_start,error_group,error_code,job_runtime FROM alertjoblist WHERE run_status=2"
__sql_timeout_log="SELECT starttime FROM alertjoblog WHERE job_id=%s order by id desc"
__alert_timeout_content="您的job(job_%s %s)在开始运行,预计时长%s分钟,但是目前仍然在运行"
def monitor():
    '''找出5分钟前应该运行却没有运行的job'''
    currentTime=time.time()-5*60
    mysqltarget=mysqlOpe()
    jobnotruninfo=mysqltarget.select(__sql_notrun%currentTime)
    for itemnotrun in jobnotruninfo:
        alertcontent=__alert_notrun_content%(itemnotrun[0],itemnotrun[1],formattime(itemnotrun[2]))
        groupid=itemnotrun[3]
        errorid=itemnotrun[4]
        mysqltarget.insert(__sql_alert_insert%(1,errorid,groupid,alertcontent,'',0,getLocalDate()))
    currentTime=time.time()
    '''查找运行超时的job'''
    jobtimeoutinfo=mysqltarget.select(__sql_timeout)
    for itemtimeout in jobtimeoutinfo:
        loginfo=mysqltarget.selectone(__sql_timeout_log%itemtimeout[0])
        if (currentTime-formatdate(loginfo[0]))>(itemtimeout[5]*60):
            alertcontent=__alert_timeout_content%(itemtimeout[0],itemtimeout[1],itemtimeout[5])
            groupid=itemnotrun[3]
            errorid=itemnotrun[4]
            mysqltarget.insert(__sql_alert_insert%(1,errorid,groupid,alertcontent,'',0,getLocalDate()))

    mysqltarget.close()


def formattime(ftime):
    return time.strftime('%Y/%m/%d %H:%M',time.localtime(ftime))

def formatdate(fdate):
    return int(time.mktime(time.strptime(fdate, '%Y-%m-%d %H:%M:%S')))

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    logging.config.fileConfig("JobsProject/log4p.conf")
    logger = logging.getLogger("main")
    sys.exit(monitor())