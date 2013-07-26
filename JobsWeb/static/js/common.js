;
var EventBind = {
    init: function () {
        this.login();
        this.loginout()
    },
    login: function () {
        var that = this;
        $('#userlogin').on('click', function (event) {
            event.preventDefault();
            $.layer({
                type: 1,
                offset: ['100px', ''],
                shade: ['', '', true],
                title: ['登陆', true],
                area: ['450px', 'auto'],
                page: {dom: '#login'}
            });
        });
        $(".loginaction").click(function (event) {
            event.preventDefault();
            var username = $.trim($("#username").val());
            var password = $.trim($("#password").val());
            if (username.length <= 0) {
                that.alert("用户名不能为空");
                return false;
            } else if (password.length <= 0) {
                that.alert("登录密码不能为空");
                return false;
            }
            commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: {type: 'login', un: username, pw: password}}, EventBind.callback, 'login');
        });
        $("#password").keydown(function (event) {
            var curKey = event.which;
            if (curKey == 13) {
                $(".loginaction").click();
            }
        });
    },
    loginout: function () {
        var that = this;
        $(".loginout").click(function () {
            commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: {type: 'loginout'}}, EventBind.callback, 'loginout');
        });
    },
    callback: function (data) {
        var extra = data.extra;
        var res = data.data;
        if (extra == "login") {
            if (res['code'] == 0) {
                urilocation(window.location.href);
            } else {
                EventBind.alert(res['message']);
            }
        } else if (extra == "loginout") {
            urilocation(window.location.href);
        } else if (extra == "deletejob") {
            EventBind.alert(res['message']);
            if (res['code'] == 0) {
                urilocation(window.location.href);
            }
        }
    },
    alert: function (msg) {
        alert(msg);
    },
    deleteJob: function (id) {
        commonajax.ajaxpost("/actioncenter/", {dataType: 'json', data: {type: 'deletejob', "id": id}}, EventBind.callback, 'deletejob');
        return false;
    }
}
$(document).ready(function () {
    EventBind.init();
});

