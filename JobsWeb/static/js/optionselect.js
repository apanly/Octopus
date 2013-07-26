;
/********js 联动插件***********/
var relationSelect = {
    init: function (parent, child) {
        this.parent = parent;
        this.child = child;
        this.initParent();
    },
    initParent: function () {
        var that=this;
        var target = $("#"+this.parent);
        $(target).change(function(){
            that.childChange();
        });
    },
    childChange: function () {
       var selectVal= $.trim($("#"+this.parent).val());
       var target=$("#"+this.child);
       var tmpoption="<option value=\"0\">请选择</option>";
       if(selectVal!=0){
            for(var index in this.data){
                if(this.data[index][0]==selectVal){
                    tmpoption+="<option value='"+this.data[index][0]+"'>"+this.data[index][1]+"</option>";
                }
            }
       }
       $(target).html(tmpoption);
    },
    setData: function (item) {
        if (this.data == undefined) {
            this.data = new Array();
        }
        this.data.push(item);
    }
};
$(document).ready(function () {
    relationSelect.init("env", "server");
});
