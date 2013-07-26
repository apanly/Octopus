;
var jobnew = {
    init: function () {
        jobnew.dependajax=0;
        this.eventBind();
        this.autofix();
    },
    eventBind: function () {
        var that = this;
        $("#runtime").datetimepicker({
            format: 'yyyy-mm-dd hh:ii',
            autoclose: true,
            startView: 0
        });
        $("#runrangetime").datetimepicker({
            format: 'hh:ii',
            autoclose: true,
            startView: 0
        });
        $("#runpertime").datetimepicker({
            format: 'hh:ii',
            autoclose: true,
            startView: 0
        });
        $("#jobenv").change(function () {
            postdata={};
            postdata.type="getjobtype";
            postdata.jobenv=that.getVal("jobenv");
            commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: postdata}, jobnew.callback, postdata.type);
        });
        $('#jobdependselect').on('click', function (event) {
            if(jobnew.dependajax<=0){
                postdata={};
                postdata.type="getdependjob";
                postdata.jobid=that.getVal("jobid");
                commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: postdata}, jobnew.callback, postdata.type);
                event.preventDefault();
            }else{
                jobnew.popindex=$.layer({
                    type: 1,
                    offset: ['100px', ''],
                    shade: ['', '', true],
                    title: ['选择依赖JOB', true],
                    area: ['800px', 'auto'],
                    page: {dom: '#selectdependjobdiv'}
            });
            }

        });
        $("#selectdependjobdiv button").click(function(){
            var tmpjobids="";
            $("#selectdependjobdiv #choosed input[name='dependjoblist']").each(function(){
                tmpjobids+= $(this).val()+",";
            });
            tmpjobids=tmpjobids.substring(0,tmpjobids.length-1);
            $("#dependjob").val(tmpjobids);
            layer.close(that.popindex);
        });
        $("#addnewjob").click(function () {
            var jobname = that.getVal("jobname");//job名称
            var jobenv=that.getVal("jobenv");//job的运用环境
            var jobserver = that.getVal("jobserver");//job运行的servername
            var command = that.getVal("command");//job运行的命令
            var is_manage = that.getVal("is_manage");//job是否需要调度
            var runtime = that.getVal("runtime");//job的运行时间
            var runrangetime = that.getVal("runrangetime");//job的运行时长
            var runpertime = that.getVal("runpertime");//job的运行间隔时间
            var dependjob = that.getVal("dependjob");//所依赖的job
            var curpath=that.getVal("curpath");//请输入游标地址
            var logpath = that.getVal("logpath");//job的日志地址
            var belong = that.getVal("belong");//job所属单位
            var owner = that.getVal("owner");//job的负责人
            var ownerid = that.getVal("ownerid");//job的负责人
            var relator = that.getVal("relator");//job的相关人
            var relatorid = that.getVal("relatorid");//job的相关人
            var jobpart = that.getVal("jobpart");//job的角色也就是作用
            var remark = that.getVal("remark");//job的备注
            if (jobname.length <= 0) {
                that.tips(0, "请输入job的名称", 1);
                that.inputfocus(0);
                return
            } else {
                that.tips(0, "*", 1);
            }
            if(jobenv==0){
                that.tips(1, "请选择job的运行环境", 1);
                that.inputfocus(0);
                return
            }else{
                 that.tips(1, "*准确指定JOB的部署、运行环境，避免不同机器环境所产生的问题", 0);
            }
            if (jobserver == 0) {
                that.tips(2, "*请选择服务器", 1);
                return
            } else {
                that.tips(2, "*", 1);
            }
            if (command.length <= 0) {
                that.tips(3, "请输入job调度命令", 1);
                that.inputfocus(1);
                return
            } else {
                that.tips(3, "*", 1);
            }
             //4 ingnore is_manage
            if(runtime.length<=0){
                that.tips(5, "*请选择运行时间", 1);
                that.inputfocus(2);
                return
            }else{
                that.tips(5, "*", 1);
            }
            if(runrangetime.length<=0){
                that.tips(6, "*请选择运行时长", 1);
                that.inputfocus(3);
                return
            }else{
                that.tips(6, "*", 1);
            }
            if(runpertime.length<=0){
                that.tips(7, "*请选择运行间隔", 1);
                that.inputfocus(4);
                return
            }else{
                that.tips(7, "*", 1);
            }
             //8 ingnore dependjob
             //9 ingnore curpath
             //10 ingnore logpath
            if (belong == 0) {
                that.tips(8, "*请选择所在部门", 1);
                return
            } else {
                that.tips(8, "*", 1);
            }
            if(owner.length<=0 || ownerid.length<=0){
               that.tips(9, "*请选择责任人", 1);
               return
            }else{
                that.tips(9, "*", 1);
            }
            if(relator.length<=0 || relatorid.length<=0){
               that.tips(10, "*请选择相关人,建议填写上级leader", 1);
               return
            }else{
                that.tips(10, "*", 1);
            }
            postdata = {};
            var jobid=parseInt(that.getVal("jobid"));
            if(jobid>0){
              postdata.type = "editjob";
              postdata.jobid = jobid;
            }else{
              postdata.type = "addnewjob";
            }
            postdata.jobname = jobname;
            postdata.jobenv=jobenv;
            postdata.jobserver = jobserver;
            postdata.command = command;
            postdata.is_manage = is_manage;
            postdata.runtime = runtime;
            postdata.runrangetime = runrangetime;
            postdata.runpertime = runpertime;
            postdata.dependjob=dependjob;
            postdata.logpath = logpath;
            postdata.curpath = curpath;
            postdata.belong = belong;
            postdata.owner = owner;
            postdata.ownerid = ownerid;
            postdata.relator = relator;
            postdata.relatorid = relatorid;
            postdata.jobpart = jobpart;
            postdata.remark = remark;
            commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: postdata}, jobnew.callback, postdata.type);
        });
    },
    getVal: function (id) {
        return $.trim($("#" + id).val());
    },
    callback: function (res) {
        var type=res.extra;
        if(type=="editjob"){
            if(res.data['code']==0){
              urilocation(window.location.href);
            }else{
              EventBind.alert(res.data['message']);
            }
        }else if(type=="addnewjob"){
            if(res.data['code']==0){
              urilocation("/job/edit/?id="+res.data['message']);
            }else{
              EventBind.alert(res.data['message']);
            }
        }else if(type=="getjobtype"){
            var data=res.data;
            $("#jobserver").empty();
            $("<option value=\"0\">请选择服务器</option>").appendTo("#jobserver");
            for(var i in data){
                $("<option value='"+data[i][0]+"'>"+data[i][1]+"</option>").appendTo("#jobserver");
            }
        }else if(type=="getdependjob"){
            var data=res.data;
            if(data.length<=0){
                alert("目前您还没有其他job可供依赖选择");
                return;
            }
            var targetid="#choose .row-fluid";
            var choosedtargetid="#choosed .row-fluid";
            var job_id=jobnew.getVal("jobid");
            var tmpdependids=new Array();
            if(job_id){
                tmpdependids=jobnew.getVal("dependjob").split(",");
            }
            $(targetid).empty();
            $(choosedtargetid).empty();
            $("<li class=\"nav-header\">JOB选择</li>").appendTo(targetid);
            $("<li class=\"nav-header\">已选JOB</li>").appendTo(choosedtargetid);
            for(var i in data){
                if($.inArray(data[i][0]+"",tmpdependids)>-1){
                   $("<li class=\"span6 marginfix\" > <label class=\"checkbox\"> <input name='dependjoblist' type=\"checkbox\"  checked value='"+data[i][0]+"'>"+data[i][1]+"</label></li>").appendTo(choosedtargetid);
                }else{
                   $("<li class=\"span6 marginfix\" > <label class=\"checkbox\"> <input name='dependjoblist' type=\"checkbox\" value='"+data[i][0]+"'>"+data[i][1]+"</label></li>").appendTo(targetid);
                }
            }
            jobnew.chooseevent();
            jobnew.choosedevent();
            jobnew.dependajax=1;
            jobnew.popindex=$.layer({
                type: 1,
                offset: ['100px', ''],
                shade: ['', '', true],
                title: ['选择依赖JOB', true],
                area: ['800px', 'auto'],
                page: {dom: '#selectdependjobdiv'}
            });
            $("#choosed").css({height:$("#choose").height()});
        }
    },
    tips: function (index, msg, redflag) {
        var target = $(".form-horizontal .control-group .tips");
        if (redflag) {
            msg = "<font color='red'>" + msg + "</font>"
        }
        $(target.get(index)).html(msg);
    },
    inputfocus: function (index) {
        var target = $(".form-horizontal .control-group input");
        $(target.get(index)).focus();
    },
    autofix: function () {
        options={
            source: function (request, response) {
                $.ajax({
                    url: "/actioncenter/",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        type: "getinfo",
                        maxRows: 12,
                        q: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                label: item[1],
                                value: item[0]
                            }
                        }));
                    }
                });
            },
            minChars: 1,
            max: 5,
            scroll: true,
            autoFill: true,
            mustMatch: true,
            matchContains: false,
            scrollHeight: 50,
            select:function( event, ui ){
                if($(this).attr("id")=="owner"){
                    $("#owner").val(ui.item.label)
                    $("#ownerid").val(ui.item.value)
                }else{
                    $("#relator").val(ui.item.label)
                    $("#relatorid").val(ui.item.value)
                }
                return false;
            }
        };
        //添加autocomplete
        $("#relator").autocomplete(options);
        $("#owner").autocomplete(options);
    },
    chooseevent:function(){
        $("#choose  input").each(function(){
            $(this).unbind("click");
            $(this).bind("click",function(){
                var target=$(this).parent().parent();
                $(target).clone().appendTo("#choosed .row-fluid");
                $(target).remove();
                jobnew.choosedevent();
            });
        });
    },
    choosedevent:function(){
        $("#choosed  input").each(function(){
            $(this).unbind("click");
            $(this).bind("click",function(){
                var target=$(this).parent().parent();
                $(target).clone().appendTo("#choose .row-fluid");
                $(target).remove();
                jobnew.chooseevent();
            });
        });
    }
};
$(document).ready(function () {
    jobnew.init();
});

