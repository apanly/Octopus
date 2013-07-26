Octous(八爪鱼)JOB调度与管理平台

一、目标
	1、优化原有WEB界面和功能
		JOB增加用户端/客户端属性
		JOB增加失败是否运行自动重启属性
		JOB增加是否支持并发属性
		WEB界面增加JOB临时运行接口
		WEB界面增加JOB运行日志查看
	2、调整报警标准
		无正确返回值则认定进程调度/运行故障
	3、调度系统增加分布式支持

二、依赖
	linux + python2.6+ + mysql5.0+
	1、django1.5+
	2、apscheduler
	3、pyzmq
	4、*zkpython
	5、websocket

三、结构
Octopus\
	JobsScript\    JOB调度command界面
		1、机器注册/注销 main.py           worker机器入口
			向db注册机器名、运行环境
			将jqueueprod、jqueuecons、logger、jmonitor注册到crontab（/var/spool/cron/<user>）
			常驻，定时更新机器信息及其负载状况（如果机器信息长时间得不到更新，worker机从调度列表中除名）
		2、队列生成 jqueueprod.py
			取job list信息，将所有需要调度到动作记录到job queue
		3、队列消费 jqueuecons.py
			每次取一条job queue，以及更新remote cursor到local cursor，并执行调度动作，退出时更新local cursor到remote cursor
			调度格式："cmd opts args_with_localcursor >> log" & "tail -f log | logger" & "cursor localcursor"
			说明： 《更新本地游标值后》 起任务并写日志 & 收集日志 & 更新远端（DB）中游标值 《更新远端游标值》
		4、日志收集 logger.py
			日志管理
			将标准输出到内容记录到db
		5、调度监控 jmonitor.py           
			监控db中日志，遇到需报警级别到日志，则生成报警请求（考虑相邻报警合并）
			定期清理过期日志
		6、日志服务 ws.py                 websocket入口
			接收mq过来到日志
			通过webseocke server发送出去
		7、游标管理 cursor.py
			及时更新local cursor到remote cursor
		8、*手动管理job sh.py             命令入口
	JobsWeb\       JOB调度web界面
		1、用户登陆验证
		2、用户审计
		3、job登记编辑/查看
		4、job查找
		5、实时日志输出
		6、3天历史日志查找
	JobsProject\   配置
	django\        django库

四、架构
	1、日志查看
			前端由websocket客户端持续接收log内容 wclogger.html
	2、日志提供
			后端由websocket服务端持续发送log内容 wslogger.y(pull)  ws://......:12345/......
	3、日志收集
			调度器将标准输出stdout内容发送给zmq，同时写入数据库（保留三天） logger.py(push)
	4、日志格式
		<时间> <名称> <级别> <内容>
		print "2013/07/04:16:41:00 app_name error Process has exited!"
	5、日志级别
		fatal error warn info debug trace all none             100start 110heartbeat 120end

五、部署
	1、开发
		# git clone ...... ./Octopus
		# useradd octopus
		# chown -R octopus:root ./Octopus
		# su octopus                                                                                 使用专用帐号
		$ cd ./Octopus
		$ echo "export PYTHONPATH=`pwd`" >> ~/.bashrc
		$ echo "export DJANGO_SETTINGS_MODULE=JobsProject.settings" >> ~/.bashrc
		$ suorce .
		$ echo "create database jobs_db character set utf8;" | mysql -uroot
		$ echo "source JobsWeb/sql/usercenter.sql" | mysql -uroot
		$ python manage.py validate
		$ python manage.py sqlall JobsWeb
		$ python manage.py syncdb
		$ python manage.py runserver                                                                 启动web服务
		$ python JobsScript/main.py localhost php5.4+,python2.6+,java1.5+ | JobsScript/logger.py     启动worker服务
		$ python JobsScript/ws.py | JobsScript/logger.py                                             启动websocket服务
		$ #########################################################################################################添加JOB
	2、生产

