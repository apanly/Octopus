;
var joblist={
    init:function(){
          this.eventInit();
          this.getJobUserList();
    },
    eventInit:function(){
    },
    getJobUserList:function(){
        postdata={};
        postdata.type="getjobuserlist";
        commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: postdata}, joblist.callback, postdata.type);
    },
    callback:function(res){
       var type=res.extra;
       var data=res.data;
       if(type=="getjobuserlist"){
            $("#owner").empty();//清空下拉框//$("#select").html('');
            $("<option value=\"0\">请选择责任人</option>").appendTo("#owner");
            for(var i in data){
                $("<option value='"+data[i][0]+"'>"+data[i][1]+"</option>").appendTo("#owner");
            }
       }
    }
}

$(document).ready(function () {
    joblist.init();
});

