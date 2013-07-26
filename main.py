import sys, os, getopt, re

import time, getpass

import JobsWeb.models


def daemon():
	opts,args=getopt.getopt(sys.argv[1:],"")
	if len(args)!=2:
		print "Uasge: %s <host_name> <host_env>\n" % sys.argv[0]
	
	pid=os.fork()
	if pid==-1:
		print "fork fail 1\n"
	elif pid>0:
		exit(0)
	
	os.setsid()
	
	pid=os.fork()
	if pid==-1:
		print "fork fail 2\n"
	elif pid>0:
		exit(0)

	os.umask(0)

	
def regcron():
	path=os.path.split(os.path.realpath(__file__))[0]
	print "update Alerthostlist set name=%s, env=%s"
	print "update crontab"
	cron="""####worker<####
00 * * * * {path}/jqueueprod.py
00 * * * * {path}/jqueuecons.py
#00 * * * * {path}/logger.py
00 * * * * {path}/jmonitor.py
####worker>####""".format(path=path)
	os.system('touch /var/spool/cron/'+getpass.getuser())
	cronf=open('/var/spool/cron/'+getpass.getuser(),'r')
	crons=cronf.read()
	cronf.close()
	cronf=open('/var/spool/cron/'+getpass.getuser(),'w')
	reg=re.compile('####worker<####[\s\S]*####worker>####')
	crons=reg.sub(cron,crons)
	cronf.write(crons)
	cronf.close()


def updb():
	while 1:
		time.sleep(1)
		print "heartbeat"
		print "update Alerthostlist set time=%s"


def do():
	regcron()
	updb()


def main():
	daemon()
	do()


if __name__ == "__main__":
	sys.exit(main())

__all__ = []
