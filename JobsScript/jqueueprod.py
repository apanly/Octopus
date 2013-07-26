# -*- coding:utf-8 -*-
import os,sys, logging, logging.config
import time
import JobsWeb.models


def main():
    logger.info("get job list")
    kwargs={"run_status":1}
    kwargs['is_manage']=1
    kwargs['runstat']=1
    kwargs['server']=1 #根据每个机器进行填写
    joblist=JobsWeb.models.Alertjoblist.objects.filter(**kwargs).order_by('id')
    currentTime=int(time.time())
    for item in joblist:
        checkJobValid(item,currentTime)

def checkJobValid(data,currentTime):
    if not data.command:
        logger.info("job id:%s 没有调度命令"%data.id)
    firstTime=data.job_first_start
    if currentTime<firstTime:
        logger.info("job id:%s 还没有到运行时间"%data.id)
    intervalTime=currentTime-data.job_first_start
    jobinterValTime=data.job_runinterval*60
    jobinterValTime=1
    if intervalTime%jobinterValTime==0:
        if data.dependjob==1:
            if checkDependJob(data.id):
                inQueue(data)
        else:
            logger.info("job id:%s 可以进入队列了"%data.id)
            inQueue(data)

    else:
        pass

def checkDependJob(jobid):
    dependjobinfo=JobsWeb.models.Alertjoblist.objects.filter(job_id=jobid)
    dependFlag=True
    for item in dependjobinfo:
        if item.run_status == 2:
            dependFlag=False
    return dependFlag


def inQueue(data):
    jobid=data.id
    server=data.server
    p= JobsWeb.models.Alertjobqueue(
        job_id=jobid,
        status=0,
        server=server,
        create_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    )
    p.save()
    logger.info("job id:%s 进入队列成功"%data.id)

if __name__ == "__main__":
	logging.config.fileConfig("JobsProject/log4p.conf")
	logger = logging.getLogger("main")
	sys.exit(main())


__all__ = []
