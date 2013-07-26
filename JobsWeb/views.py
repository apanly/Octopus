# -*- coding:utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.contrib import auth
import re
import time
import JobsWeb.settings

import JobsWeb.models


def home(request):
    uid=userAuth(request)
    if uid :
        pageSize=10 
        req=request.GET
        if 'page' in req and req['page']:
            page=int(req['page'])
        else:
            page =1
        joblist = JobsWeb.models.Alertjoblist.objects.filter(owner=uid,runstat=1).order_by("-id")
        responsedata={}
        responsedata['jobcnt']=len(joblist)
        offsettmp=(page-1)*pageSize
        limittmp =pageSize*page
        pagecnt=ceil(responsedata['jobcnt'],pageSize)
        responsedata['joblist']=joblist[offsettmp:limittmp]
        responsedata['usertem']=userinfoTem(request)
        responsedata['paginationTem']=paginationTem(page, pagecnt,"/home/?")
        serverlist = JobsWeb.models.Alertjobhost.objects.all()
        tmplist=[]
        for item in responsedata['joblist']:
            tmpuserinfo=getUserInfo(int(item.owner),'','')
            item.owner=tmpuserinfo.UserName
            item.job_first_start=time.strftime('%Y/%m/%d %H:%M',time.localtime(item.job_first_start))
            for server in serverlist:
                if int(item.server) == server.id:
                    item.server=server.name
                    item.env=server.env
                    tmplist.append(item)
                    break
        #responsedata['joblist']=tmplist
        responsedata['serverlist']=serverlist
        return render_to_response('home.html',responsedata)
    else:
        return HttpResponseRedirect("/joblist/")


def joblist(request):
    uri="/joblist/?"
    req=request.GET
    joblist = JobsWeb.models.Alertjoblist.objects.filter(runstat=1).order_by("-id")
    kwargs={"runstat":1}
    if "mutimode" in req and req['mutimode']:
        pattern = re.compile(r'^\d+$')
        match = pattern.match(req['mutimode'])
        if match:
            kwargs['id']=int(req['mutimode'])
            uri +="&jobid=%d"%kwargs['id']
        else:
            kwargs['name__contains']='%s'%req['mutimode']
            uri +="&jobname=%s"%kwargs['name__contains']
    else:
        if 'jobid' in req and req['jobid']:
            kwargs['id']=int(req['jobid'])
            uri +="&jobid=%d"%kwargs['id']

        if 'server' in req and int(req['server']):
            kwargs['server']=int(req['server'])
            uri +="&server=%d"%kwargs['server']

        if 'owner' in req and int(req['owner']):
            kwargs['owner']=int(req['owner'])
            uri +="&owner=%d"%kwargs['owner']

        if 'belong' in req and req['belong']:
            kwargs['site']=int(req['belong'])
            uri +="&belong=%d"%kwargs['site']

        if 'is_manage' in req and req['is_manage']:
            kwargs['is_manage']=int(req['is_manage'])
            uri +="&is_manage=%d"%kwargs['is_manage']

        if 'jobname' in req and req['jobname']:
            kwargs['name__contains']='%s'%req['jobname']
            uri +="&jobname=%s"%kwargs['name__contains']


    joblist = JobsWeb.models.Alertjoblist.objects.filter(**kwargs).order_by("-id")
    responsedata={}
    responsedata['jobcnt']=len(joblist)
    responsedata['usertem']=userinfoTem(request)
    '''
      分页逻辑start
    '''
    pageSize=10
    req=request.GET
    if 'page' in req and req['page']:
        page=int(req['page'])
    else:
        page =1
    offsettmp=(page-1)*pageSize
    limittmp =pageSize*page
    pagecnt=ceil(responsedata['jobcnt'],pageSize)
    responsedata['joblist']=joblist[offsettmp:limittmp]
    responsedata['page']=page
    responsedata['paginationTem']=paginationTem(page, pagecnt,uri)
    '''
      分页逻辑end
    '''
    serverlist = JobsWeb.models.Alertjobhost.objects.all()
    responsedata['serverlist']=serverlist
    tmplist=[]
    for item in responsedata['joblist']:
        for server in serverlist:
            if int(item.server) == server.id:
                tmpuserinfo=getUserInfo(int(item.owner),'','')
                item.server=server.name
                item.owner=tmpuserinfo.UserName
                item.env=server.env
                item.job_first_start=time.strftime('%Y/%m/%d %H:%M',time.localtime(item.job_first_start))
                tmplist.append(item)
                break
    responsedata['joblist']=tmplist
    responsedata['searchdata']=kwargs
    return render_to_response('listjob.html',responsedata)


def tools(request):
    responsedata={}
    responsedata['usertem']=userinfoTem(request)
    
    req=request.GET
    if 'type' in req and req['type']:
        type=req['type']
    else:
        type="runlist"
    if type =="showlog":
        if 'id' in req:
	        responsedata['filter']='id:'+req['id']
        if 'line' in req:
	        responsedata['line']=req['line']
        else:
	        responsedata['line']=20
        responsedata['host']=JobsWeb.settings.WS_URL
        return render_to_response('wclogger.html',responsedata)
    return render_to_response('tools.html',responsedata)


def logger(request):
	responsedata={}
	responsedata['usertem']=userinfoTem(request)
	responsedata['filter']=''
	responsedata['line']=20
	responsedata['host']=JobsWeb.settings.WS_URL
	return render_to_response('wclogger.html',responsedata)


def jobview(request):
    responsedata={}
    responsedata['usertem']=userinfoTem(request)
    return render_to_response('jobview.html',responsedata)

def jobnew(request):
    uid=userAuth(request)
    if not uid :
        return HttpResponseRedirect("/joblist/")
    responsedata={}
    envlist = JobsWeb.models.Alertjobhost.objects.all()
    envlist.query.group_by = ['env']
    serverlist = JobsWeb.models.Alertjobhost.objects.all()
    responsedata['envlist']=envlist
    responsedata['serverlist']=serverlist
    responsedata['usertem']=userinfoTem(request)
    return render_to_response('jobnew.html',responsedata)

def jobedit(request):
    uid=userAuth(request)
    if not uid :
        return HttpResponseRedirect("/joblist/")
    req=request.GET
    if 'id' in req and req['id']:
        jobid=req['id']
    else:
        jobid=0
    responsedata={}
    envlist = JobsWeb.models.Alertjobhost.objects.all()
    responsedata['envlist']=envlist
    jobinfo=JobsWeb.models.Alertjoblist.objects.filter(id=jobid)[0]
    serverlist = JobsWeb.models.Alertjobhost.objects.filter(id=jobinfo.server)
    if int(jobinfo.owner) == uid :
        jobinfo.server=int(jobinfo.server)
        jobinfo.job_first_start=time.strftime('%Y-%m-%d %H:%M',time.localtime(jobinfo.job_first_start))
        tmp_job_runtime=jobinfo.job_runtime
        tmpHour=int(tmp_job_runtime/60)
        tmpMinute=int(tmp_job_runtime%60)
        tmpMinute=tmpMinute if tmpMinute>=10 else "0"+str(tmpMinute)
        jobinfo.job_runtime=''+str(tmpHour)+':'+str(tmpMinute)
        tmp_job_runinterval=jobinfo.job_runinterval
        tmpHour=int(tmp_job_runinterval/60)
        tmpMinute=int(tmp_job_runinterval%60)
        tmpMinute=tmpMinute if tmpMinute>=10 else "0"+str(tmpMinute)
        jobinfo.job_runinterval=''+str(tmpHour)+':'+str(tmpMinute)
        responsedata['serverlist']=serverlist
        jobinfo.ownerName=getUserInfo(int(jobinfo.owner),'','').UserName
        if int(jobinfo.relate_owner)>0:
            jobinfo.relateName=getUserInfo(int(jobinfo.relate_owner),'','').UserName
        tmpdependjobid=""
        if jobinfo.job_type ==3:
            dependjobinfo=JobsWeb.models.Alertjobdepend.objects.filter(job_id=jobid)

            for item in dependjobinfo:
                tmpdependjobid+=str(item.depend_id)+","
        tmpdependjobid=tmpdependjobid[0:-1]
        jobinfo.dependjobinfo=tmpdependjobid
        responsedata['jobinfo']=jobinfo
        responsedata['usertem']=userinfoTem(request)
        return render_to_response('jobnew.html',responsedata)
    else:
        return HttpResponseRedirect("/joblist/")

def alert(request):
	return render_to_response('alert.html')

def actioncenter(request):
    req=request.POST
    type=req['type']
    if type == "login":
        return userlogin(request)
    elif type == "addnewjob":
        return addnewjob(request)
    elif type == "editjob":
        return editvimjob(request)
    elif type== "loginout":
        del request.session['uid']
        del request.session['username']
        return HttpResponse(json.dumps({"code":0,"message":'success'}))
    elif type == "getinfo":
        responsedata=getUserInfo(username=req['q'],uid=0,password='')
        tmp=[]
        for item in responsedata:
            tmp.append([item.MId,item.UserName])
        return HttpResponse(json.dumps(tmp))
    elif type =="deletejob":
        return deletejob(request)
    elif type == "getjobtype":
        return getjobtype(request)
    elif type =="getjobuserlist":
        return getjobuserlist(request)
    elif type=="getdependjob":
        return getdependjob(request)


def userAuth(request):
    if 'uid' in request.session and request.session["uid"]:
        uid=request.session["uid"]
    else:
        uid=0
    return uid

def userlogin(request):
    req=request.POST
    if 'un' in req and  req['un']:
        username=req['un']
    else:
        return HttpResponse(json.dumps({"code":1,"message":'用户名不能为空'}))
    if 'pw' in req and  req['pw']:
        password=req['pw']
    else:
        return HttpResponse(json.dumps({"code":1,"message":'密码不能为空'}))
    response = HttpResponse()
    #response.set_cookie("uid",1,None,86400,"/")
    #response.set_cookie("username",username,None,86400,"/")
    loginfo=getUserInfo(username=username,password=password,uid=0)
    responsedata={}
    responsedata['code']=0
    responsedata['message']='success'
    if len(loginfo)<1:
        responsedata['code']=1
        responsedata['message']='用户名或者密码不正确'
    else:
        request.session['uid'] = loginfo[0].MId
        request.session['username']=loginfo[0].UserName
    response.write(json.dumps((responsedata)))
    return response

def userinfoTem(request):
    responsedata={}
    uid=userAuth(request)
    if uid :
        responsedata['uid']=uid
        responsedata['username']=request.session['username']
    t = get_template('userinfo.html')
    html = t.render(Context(responsedata))
    return html

def paginationTem(page,pagecnt,uri):
    responsedata={}
    responsedata['page']=page
    responsedata['pagecnt']=pagecnt
    responsedata['uri']=uri
    responsedata['pagelist']=range(1,pagecnt+1)
    if page >1:
        responsedata['prepage']=page-1
    else :
        responsedata['prepage']=False
    if page < pagecnt:
        responsedata['nextpage']=page+1
    else :
        responsedata['nextpage']=False
    t = get_template('pagination.html')
    html = t.render(Context(responsedata))
    return html

def getUserInfo(uid,username,password):
    if password:
        import base64
        import hashlib
        return JobsWeb.models.UserCenter.objects.filter(UserName='%s'%username,UserPasswd='%s'%base64.b64encode(hashlib.md5(password).hexdigest()))
    elif username :
        return JobsWeb.models.UserCenter.objects.filter(UserName__contains='%s'%username)[0:12]
    elif uid :
        return JobsWeb.models.UserCenter.objects.filter(MId=uid)[0]

def ceil(x, y):
    return int((x+y-1)/y)

def addnewjob(request):
    req=request.POST
    name=req['jobname']
    server=req['jobserver']
    command=req['command']
    is_manage=req['is_manage']
    job_first_start=int(time.mktime(time.strptime(req['runtime'], '%Y-%m-%d %H:%M')))
    tmp_job_runtime=req['runrangetime'] #job预计运行时间
    tmpTimes=tmp_job_runtime.split(":")
    job_runtime=int(tmpTimes[0])*60+int(tmpTimes[1])
    tmp_job_runinterval=req['runpertime']
    tmpTimes=tmp_job_runinterval.split(":")
    job_runinterval=int(tmpTimes[0])*60+int(tmpTimes[1])
    dependjob=1 if req['dependjob'] else 0
    islog=req['logpath']
    curpath=req['curpath']
    site=req['belong']
    owner=req['ownerid']
    relate_owner=req['relatorid']
    effect=req['jobpart']
    remark=req['remark']
    run_status=1 if is_manage else 0
    queue_status=0
    runstat=1
    '''获取报警组'''
    error_group=getAlertGroup('Job_%s'%name,owner+","+relate_owner)
    error_code=0
    job_type=3 if dependjob else 0
    job_threshold_up=0
    job_threshold_down=0
    offset=0
    job_start='0'
    job_run_interval='0'
    job_interval='0'
    p= JobsWeb.models.Alertjoblist(
    name=name,
    server='%s'%server,
    command=command,
    is_manage=is_manage,
    job_first_start=job_first_start,
    job_runtime=job_runtime,
    job_runinterval=job_runinterval,
    cur_log=curpath,
    islog=islog,
    owner=owner,
    relate_owner=relate_owner,
    effect=effect,
    remark=remark,
    site=site,
    error_group=error_group,
    error_code=error_code,
    runstat=runstat,
    queue_status=queue_status,
    run_status=run_status,
    job_type=job_type,
    job_threshold_up=job_threshold_up,
    job_threshold_down=job_threshold_down,
    offset=offset,
    job_start=job_start,
    job_run_interval=job_run_interval,
    job_interval=job_interval,
    )
    p.save()
    jobid=int(p.id)
    if dependjob == 1:
            dependjobaction(p.id,str(req['dependjob']))
    #添加报警errorcode
    if jobid <10:
        errorcode = '200%d'%jobid;
    elif jobid <100:
        errorcode = '20%d'%jobid;
    else:
        errorcode = '2%d'%jobid;
    addJobErrorCode(jobid,errorcode)
    jobmodlog(p.id,owner,'新添加job,id is %d'%jobid)
    return HttpResponse(json.dumps(({'code':0,'message':jobid})))


def editvimjob(request):
    req=request.POST
    if 'jobid' in req and req['jobid']:
        jobid=req['jobid']
    else:
        jobid=0
    jobinfo = JobsWeb.models.Alertjoblist.objects.filter(id=jobid)[0]
    uid=userAuth(request)
    reponsedata={}
    reponsedata['code']=0
    reponsedata['message']='success'
    if int(jobinfo.owner) == uid :
        req=request.POST
        name=req['jobname']
        server=req['jobserver']
        command=req['command']
        is_manage=req['is_manage']
        job_first_start=int(time.mktime(time.strptime(req['runtime'], '%Y-%m-%d %H:%M')))
        tmp_job_runtime=req['runrangetime'] #job预计运行时间
        tmpTimes=tmp_job_runtime.split(":")
        job_runtime=int(tmpTimes[0])*60+int(tmpTimes[1])
        tmp_job_runinterval=req['runpertime']
        tmpTimes=tmp_job_runinterval.split(":")
        job_runinterval=int(tmpTimes[0])*60+int(tmpTimes[1])
        dependjob=1 if req['dependjob'] else 0
        islog=req['logpath']
        curpath=req['curpath']
        site=req['belong']
        owner=req['ownerid']
        relate_owner=req['relatorid']
        effect=req['jobpart']
        remark=req['remark']
        target=JobsWeb.models.Alertjoblist.objects.get(id=jobid)
        target.name=name
        target.server=server
        target.command=command
        target.is_manage=is_manage
        target.job_first_start=job_first_start
        target.job_runtime=job_runtime
        target.job_runinterval=job_runinterval
        target.job_type=3 if dependjob else 0
        target.islog=islog
        target.curpath=curpath
        target.site=site
        target.owner=owner
        target.run_status=1 if is_manage else 0
        target.relate_owner=relate_owner
        target.effect=effect
        target.remark=remark
        target.save()
        dependjobaction(jobid,req['dependjob'])
        modeAlertGroup(jobinfo.error_group,owner+","+relate_owner)
        jobmodlog(jobid,owner,'修改job')
    else:
        reponsedata['code']=1
        reponsedata['message']='不要删除不属于自己的JOB'
    return HttpResponse(json.dumps((reponsedata)))

def deletejob(request):
    req=request.POST
    jobid=req['id']
    jobinfo = JobsWeb.models.Alertjoblist.objects.filter(id=jobid)[0]
    uid=userAuth(request)
    reponsedata={}
    reponsedata['code']=0
    reponsedata['message']='success'
    if int(jobinfo.owner) == uid :
        target=JobsWeb.models.Alertjoblist.objects.get(id=jobid)
        target.runstat=0
        #target.delete()
        target.save()
    else:
        reponsedata['code']=1
        reponsedata['message']='不要删除不属于自己的JOB'
    return HttpResponse(json.dumps((reponsedata)))


def getjobtype(request):
    req=request.POST
    jobenv=req['jobenv']
    responsedata=JobsWeb.models.Alertjobhost.objects.filter(id=jobenv)
    tmp=[]
    for item in responsedata:
        tmp.append([item.id,item.name])
    return HttpResponse(json.dumps(tmp))

def getAlertGroup(name,userlist):
    p=JobsWeb.models.Alertgroup(name=name,userlist=userlist)
    p.save()
    return p.id
def addJobErrorCode(jobid,error_code):
    target=JobsWeb.models.Alertjoblist.objects.get(id=jobid)
    target.error_code=error_code
    target.save()
def modeAlertGroup(groupid,userlist):
    target=JobsWeb.models.Alertgroup.objects.get(id=groupid)
    target.userlist=userlist
    target.save()

def jobmodlog(jobid,owner,content):
    p=JobsWeb.models.Alertjobmodlog(
    job_id=jobid,
    owner=owner,
    content=content,
    mod_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    )
    p.save()

def getjobuserlist(request):
    from django.db.models import Count
    res=JobsWeb.models.Alertjoblist.objects.values('owner').annotate(cnt=Count('owner'))
    tmp=[]
    for item in res:
        tmpUname=getUserInfo(uid=item['owner'],username='',password='')
        tmp.append([item['owner'],tmpUname.UserName])
    return HttpResponse(json.dumps(tmp))


def getdependjob(request):
    uid=userAuth(request)
    req=request.POST
    jobid= req['jobid'] if req['jobid'] else 0
    if jobid >0:
        kwargs={"id":jobid}
        res=JobsWeb.models.Alertjoblist.objects.exclude(**kwargs)
        res=res.filter(runstat=1)
    else :
        kwargs={"owner":uid}
        kwargs['runstat']=1
        res=JobsWeb.models.Alertjoblist.objects.filter(**kwargs)
    tmp=[]
    for item in res:
        tmp.append([item.id,item.name])
    return HttpResponse(json.dumps(tmp))

def dependjobaction(jobid,dependjobids):
    try:
    #response = HttpResponse()
    #if 1:
        hasdependinfo=JobsWeb.models.Alertjobdepend.objects.filter(job_id=jobid)
        tmpjobid=[]
        if dependjobids:
            tmpjobid=dependjobids.split(",")
        '''删除不依赖的job'''
        if hasdependinfo:
            for hasitem in hasdependinfo:
                if tmpjobid:
                    flag=False
                    for item in tmpjobid:
                        if int(item) == int(hasitem.depend_id):
                            flag=True
                            break
                    if flag == False:
                        p = JobsWeb.models.Alertjobdepend.objects.get(id=hasitem.id)
                        p.delete()
                else:
                    p = JobsWeb.models.Alertjobdepend.objects.get(id=hasitem.id)
                    p.delete()
        '''添加新依赖的job'''
        if tmpjobid:
            for item in tmpjobid:
                if hasdependinfo:
                    flag=False
                    for hasitem in hasdependinfo:
                        if int(item) == int(hasitem.depend_id):
                            flag=True
                            break
                    if flag == False:
                        p=JobsWeb.models.Alertjobdepend(job_id=jobid,depend_id=item)
                        p.save()
                else:
                    p=JobsWeb.models.Alertjobdepend(job_id=jobid,depend_id=item)
                    p.save()
    except:
    #else:
        return
        #return response
