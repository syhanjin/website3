var user, user_data,//
    afterdata = function () { }
$(function () {
    $.cookie.raw = true;
    $.get('/api/user/data', function (rel) {
        console.log(rel)
        if (rel['code'] != 0) {
            // alert('t');
            $.cookie('_uid', '', { path: '/', expires: -1 });
            $(".user .user-menu").remove();
        } else {
            rel = rel['data']
            // alert($.cookie('_uid'));
            $.cookie('_uid', $.cookie('_uid'), {
                expires: 3,
                path: '/'
            });
            // 处理用户名和头像 .user-photo 默认生成为用户头像
            user = rel['user'];
            $(".oper").remove();
            var p = $(".user-photo");
            p.prepend('<img src="' + rel['photo'] + '" />');
            // .user-name 默认生成为用户名 如果是a标记，自动添加链接
            $(".user-name").append(rel['user']);
            $("a.user-name").get(0).href = '/user/' + rel['_uid'];
            p.show();
            // 显示在界面上的信息处理
            if (rel['chat-count']){// 聊天室未读信息
            $('.bar-chat').append('<div class="after" data-count="' +
                (rel['chat-count'] > 99 ? '99+' : rel['chat-count'])
                + '" >');
            }
            // 某些页面可能会用到信息
            user_data = rel;
            if (afterdata) afterdata();
        }
    }).fail(function () {
        $(".user .user-menu").remove();
    });
    $(".user .user-photo").hover(function () {
        $(".user .user-menu").stop();
        $(".user .user-menu").css("display", "block");
        $(".user .user-menu").animate({
            opacity: '1',
        });
    }, function () {
        $(".user .user-menu").stop();
        $(".user .user-menu").animate({
            opacity: '0',
        }, function () {
            $(".user .user-menu").css("display", "none");
        });
    });
    $(".user .user-menu").hover(function () {
        $(".user .user-menu").stop();
        $(".user .user-menu").css("display", "block");
        $(".user .user-menu").css('opacity', '1');
    }, function () {
        $(".user .user-menu").stop();
        $(".user .user-menu").animate({
            opacity: '0',
        }, function () {
            $(".user .user-menu").css("display", "none");
        });
    });

    // events
    // init_events();
})