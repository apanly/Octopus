CREATE DATABASE IF NOT EXISTS jobs_db default charset utf8 COLLATE utf8_general_ci;
CREATE TABLE `alertgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50)  NOT NULL ,
  `userlist` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
  
  CREATE TABLE `alertjobalert` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL,
  `error_type` tinyint(4) DEFAULT NULL COMMENT '????.',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `content` varchar(500) NOT NULL COMMENT '????',
  `log_id` int(11) NOT NULL,
  `stat` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjobdatasource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL COMMENT 'job?id',
  `type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '?????0??????1????',
  `operation` tinyint(1) DEFAULT '0' COMMENT '????0????1???',
  `server` varchar(50) DEFAULT NULL COMMENT '???',
  `dbname` varchar(50) DEFAULT NULL COMMENT '?????',
  `dbtable` varchar(50) DEFAULT NULL COMMENT '?????',
  `other` varchar(500) DEFAULT NULL COMMENT '????',
  `mod_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjobdepend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL COMMENT 'jobid',
  `depend_id` int(11) DEFAULT NULL COMMENT '????job_id',
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjobdeploy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL,
  `content` varchar(300) DEFAULT NULL COMMENT '????',
  `deployfile` varchar(100) DEFAULT NULL COMMENT '????',
  `stat` tinyint(4) DEFAULT NULL COMMENT '????',
  `mod_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjoberror` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL,
  `error_id` int(11) NOT NULL COMMENT '���м�¼alertjoblog������id',
  `findtime` datetime DEFAULT NULL COMMENT '????',
  `reason` varchar(500) DEFAULT NULL COMMENT '????',
  `errorresult` varchar(500) DEFAULT NULL COMMENT '??',
  `errorlevel` varchar(10) DEFAULT NULL COMMENT '????',
  `process` varchar(500) DEFAULT NULL COMMENT '????',
  `finetime` datetime DEFAULT NULL COMMENT '????',
  `mod_time` timestamp NULL DEFAULT NULL,
  `error_type` tinyint(4) NOT NULL COMMENT '????',
  `stat` tinyint(4) NOT NULL COMMENT '???? 0??? 1???',
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjoblist` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `code` varchar(10) NOT NULL,
 `name` varchar(100)  DEFAULT NULL COMMENT 'job的名字',
 `server` varchar(100) DEFAULT NULL COMMENT 'job所在的服务器',
 `effect` varchar(500) DEFAULT NULL COMMENT 'job的作用',
 `owner` varchar(100) DEFAULT NULL COMMENT 'job的责任人',
 `relate_owner` varchar(100) DEFAULT NULL COMMENT 'job相关人',
 `runstat` tinyint(4) DEFAULT '0' COMMENT '是否可见',
 `iswatch` tinyint(4) DEFAULT NULL,
 `watchmethod` varchar(500) NOT NULL,
 `islog` varchar(100)  DEFAULT NULL COMMENT '日志地址',
 `dbstat` varchar(500) DEFAULT NULL,
 `ontime` varchar(100) DEFAULT NULL COMMENT '上线时间',
 `remark` varchar(500) DEFAULT NULL COMMENT '备注',
 `read_db` varchar(500) DEFAULT NULL COMMENT '?????',
 `write_db` varchar(500) DEFAULT NULL,
 `mod_time` timestamp NULL DEFAULT NULL,
 `job_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1定时2常驻3定时加常驻 4完全依赖',
 `job_start` varchar(10) NOT NULL COMMENT '老job 运行时间',
 `job_expected_end` varchar(10) DEFAULT NULL COMMENT '老job 运行时长',
 `dependjob` tinyint(1) NOT NULL COMMENT '1表示依赖job',
 `job_threshold_up` tinyint(4) NOT NULL DEFAULT '0',
 `job_threshold_down` tinyint(4) NOT NULL DEFAULT '0',
 `job_end` varchar(10) NOT NULL,
 `offset` tinyint(3) NOT NULL DEFAULT '0' COMMENT '偏移量',
 `job_max_times` int(5) DEFAULT NULL,
 `job_run_interval` varchar(10) NOT NULL,
 `job_interval` varchar(10) NOT NULL,
 `job_interval_type` tinyint(1) DEFAULT '1',
 `command` varchar(255)  DEFAULT NULL COMMENT '调度命令',
 `business_level` varchar(3) NOT NULL COMMENT '业务级别',
 `run_time_level` varchar(10) DEFAULT NULL COMMENT '时间级别',
 `data_source` varchar(500) DEFAULT NULL,
 `run_status` tinyint(1) DEFAULT '0' COMMENT '运行状态1：运行中 0 没运行',
 `queue_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '队列状态 1：队列中 0 没在队列',
 `is_manage` tinyint(1) DEFAULT '1' COMMENT '是否调度',
 `delete_log` varchar(500) DEFAULT NULL COMMENT '删除日志的方法',
 `cur_log` varchar(200)  NOT NULL COMMENT '游标文件地址',
 `error_group` int(10) NOT NULL COMMENT '报警组',
 `error_code` int(10) NOT NULL COMMENT '报警code',
 `site` tinyint(3) NOT NULL COMMENT '1客户端 2用户端',
 `job_first_start` int(10) NOT NULL COMMENT 'job第一次运行的时间戳',
 `job_runtime` int(10) NOT NULL COMMENT 'job运行时长单位分钟',
 `job_runinterval` int(10) NOT NULL COMMENT 'job间隔时间单位分钟',
 PRIMARY KEY (`id`),
 KEY `queue_status` (`queue_status`),
 KEY `owner` (`owner`),
 KEY `runstat` (`runstat`),
 KEY `name` (`name`),
 KEY `server` (`server`),
 KEY `command` (`command`),
 KEY `job_start` (`job_start`)
);

CREATE TABLE `alertjoblist_old` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `server` varchar(100) DEFAULT NULL,
  `runtime` varchar(100) DEFAULT NULL,
  `effect` varchar(255) DEFAULT NULL,
  `owner` varchar(100) DEFAULT NULL,
  `runstat` tinyint(4) DEFAULT NULL,
  `iswatch` tinyint(4) DEFAULT NULL,
  `isrecover` tinyint(4) DEFAULT NULL,
  `islog` tinyint(4) DEFAULT NULL,
  `dbstat` varchar(255) DEFAULT NULL,
  `ontime` varchar(100) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjoblog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL,
  `starttime` timestamp NULL DEFAULT NULL COMMENT 'job??????',
  `endtime` timestamp NULL DEFAULT NULL COMMENT 'job??????',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '����״̬0Ϊ��1Ϊ�쳣',
  PRIMARY KEY (`id`),
  KEY `idx_1` (`job_id`,`starttime`)
);

CREATE TABLE `alertjoblog_old` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjobmodlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) DEFAULT NULL COMMENT 'jobid',
  `owner` varchar(50) DEFAULT NULL COMMENT '修改人id',
  `ontime` varchar(50) DEFAULT NULL COMMENT '',
  `content` varchar(500)  NOT NULL COMMENT '内容',
  `mod_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertjobqueue` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `job_id` int(10) NOT NULL COMMENT '????job?id',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '????job???0????1????-1?????',
  `pid` int(10) DEFAULT NULL COMMENT '??job?id,???job??????,???,???',
  `server` varchar(100) NOT NULL COMMENT '?????????job',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '????',
  PRIMARY KEY (`id`),
  KEY `server` (`server`,`status`),
  KEY `idx_1` (`job_id`,`create_time`)
);

CREATE TABLE `alertjobrunlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL COMMENT 'job��id',
  `content` varchar(255) NOT NULL COMMENT '��¼������',
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`)
);

CREATE TABLE `alertjobsystem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cpu` float NOT NULL COMMENT 'cpuʹ����',
  `memory` float NOT NULL COMMENT '�ڴ�ʹ����',
  `server` varchar(255) NOT NULL COMMENT '���������',
  PRIMARY KEY (`id`),
  KEY `cpu` (`cpu`,`memory`)
);

CREATE TABLE `alertlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `level_id` tinyint(4) DEFAULT NULL COMMENT '1??? 2???',
  `module_id` int(11) DEFAULT NULL COMMENT '???? id',
  `group_id` int(11) DEFAULT NULL COMMENT '??????id',
  `content` varchar(255) DEFAULT NULL COMMENT '????',
  `param` varchar(500) DEFAULT NULL COMMENT '?????????',
  `stat` tinyint(4) DEFAULT '0' COMMENT '???? 0??? 1???',
  `created_time` datetime DEFAULT NULL COMMENT '????',
  PRIMARY KEY (`id`),
  KEY `stat_time` (`stat`,`created_time`)
);

CREATE TABLE `alertlogmodule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertmodule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `alertpublish` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` int(11) NOT NULL COMMENT '������id',
  `release` varchar(15) NOT NULL COMMENT '�汾���',
  `pmt` int(11) NOT NULL COMMENT 'pmt���',
  `branch` varchar(255) DEFAULT NULL,
  `review` int(11) DEFAULT NULL,
  `business_level` varchar(10) DEFAULT NULL COMMENT 'ҵ�񼶱�',
  `tech_level` varchar(10) DEFAULT NULL COMMENT '�������Ӷ�',
  `no_test` tinyint(1) NOT NULL DEFAULT '0' COMMENT '�Ƿ�Ϊnotesting,0���ǣ�1��',
  `test` int(11) DEFAULT NULL COMMENT '�����������¼�û�id',
  `second_test` int(11) DEFAULT NULL COMMENT '���β����������¼�û�id',
  `self_test` tinyint(1) DEFAULT '0' COMMENT '�Բ������0δͨ��1ͨ��',
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);
