;
var socket=null;
var linenum=1;
var util={
    setHost:function(host){
        this.host=host;
    },
    init:function(){
      this.eventInit();
      this.sconnect();
    },
    filter:function(msg,fword){
        var indexPos=msg.indexOf(fword);
        if(indexPos>=0){
           msg=msg.replace(fword,"<font color='red'>"+fword+"</font>");
           this.log(msg);
        }

    },
    log:function(msg){
            var logmsg=$("#log").html().split("\n");
            var lineFilter=parseInt($("#lines").val());
            if(logmsg.length<lineFilter){
                $("#log").append(msg+"<br/>");
            }else{
                logmsg.push(msg+"<br/>");
                logmsg.splice(0,1);
                $("#log").html("");
                $("#log").append(logmsg.join("\n"));
            }
            $("#log").scrollTop(500);
    },
    close:function(){
           if(socket!=null){
              this.log("Goodbye!");
              socket.close();
              socket = null;
           }else{
              this.log("WebSocket Has closed!");
           }

    },
    clean:function(){
        $("#log").html("");
    },
    connect:function(){
        if(socket==null){
            this.sconnect();
        }
    },
    sconnect:function(){
        var that=this;
        var host = "ws://"+this.host+"/ws.py";
            try {
                socket = new WebSocket(host);
                //this.log('WebSocket - status ' + socket.readyState);
                that.log("正在连接");
                socket.onopen = function (msg) {
                    //that.log("Welcome - status " + this.readyState);
                    that.log("连接成功");
                };
                socket.onmessage = function (msg) {
                        var fword= $.trim($("#fiter").val());
                        if(fword){//过滤
                            that.filter(msg.data,fword);
                        }else{
                            that.log(msg.data);
                        }
                };
                socket.onclose = function (msg) {
                    socket=null;
                    //that.log("Disconnected - status " + this.readyState);
                    that.log("连接失败");
                };
            }
            catch (e) {
                this.log("error");
            }
    },
    eventInit:function(){
        var that=this;
        $("#clearcls").click(function(){
           that.clean();
        });
        $("#conns").click(function(){
           that.connect();
        });
        $("#connoff").click(function(){
           that.close();
        });
    }
}
Array.prototype.remove=function(dx){
   if(isNaN(dx)||dx>this.length){
       return false;
    }
   for(var i=0,n=0;i<this.length;i++){
        if(this[i]!=this[dx]){
            this[n++]=this[i];
        }
    }
    this.length-=1;
 };
$(document).ready(function(){
    util.init();
});
