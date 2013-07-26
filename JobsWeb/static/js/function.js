;
commonajax = {
    ajaxget:function (httpurl, callback, extra) {
        $.ajax({
            type:'GET',
            url:httpurl,
            dataType:'json',
            success:function (res) {
                callback({'data':res, "extra":extra});
            }
        });
    },
    ajaxpost:function(httpurl,option,callback, extra){
        $.ajax({
            type:'POST',
            url:httpurl,
            dataType:option.dataType,
            data:option.data,
            success:function (res) {
                if(callback && typeof callback=="function"){
                    callback({'data':res, "extra":extra});
                }
            }
        });
    }
}


function urilocation(uri){
    window.location.href=uri;
}
