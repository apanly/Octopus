#!/usr/bin/python
# -*- coding:utf-8 -*-


import sys, os, time, zmq, getopt, logging, logging.config

from JobsProject.server import LOG_CLIENT
import JobsWeb.models


def main():
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.setsockopt(zmq.LINGER, 10)
    retry = 1
    while retry:
    	try:
    		sender.connect(LOG_CLIENT)
    		retry = 0
    	except:
    		logger.info("第%s次连接日志服务器失败，3秒后自动重试" % retry)
    		retry += 1
    		time.sleep(3)

    log = True
    while log:
        log = sys.stdin.readline()

        msg = log.strip()
        if msg:
			#h=JobsWeb.models.AlertjoblogOld(name='test',content=log,logtime=time.time())
			#h.save()
        	try:
        		sender.send(msg,zmq.NOBLOCK)
        	except:
        		logger.info("日志发送失败")
        	logger.info(msg)

    try:
    	sender.close()
    	context.term()
    except:
    	logger.info("未正常关闭连接")


if __name__ == "__main__":
	name = "main"

	opts,args=getopt.getopt(sys.argv[1:],None)
	if len(args)==1:
		name = args[0]
		

	path=os.path.split(os.path.realpath(__file__))[0]
	logging.config.fileConfig(path+"/../JobsProject/log4p.conf")
	logger = logging.getLogger(name)

	sys.exit(main())

__all__ = []
