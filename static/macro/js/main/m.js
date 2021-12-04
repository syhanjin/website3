$(document).ready(function () {
    $.get('/api/getuserdata', function (rel) {
        if (rel['code'] != 0) {
            $.cookie('_uid', '', {
                path: '/',
                expires: -1
            });
        } else {
            rel = rel['data'];
            // alert($.cookie('_uid'));
            $.cookie('_uid', $.cookie('_uid'), {
                expires: 3,
                path: '/'
            });
            // 处理用户名和头像 .user-photo 默认生成为用户头像
            var u = $('.nav .user');
            $(".user-photo").prepend('<img src="' + rel['photo'] + '" />');
            var info = u.children('.uinfo');
            // .user-name 默认生成为用户名 如果是a标记，自动添加链接
            $(".user-name").text(rel['user']);
            $(".nav .user .uinfo .user-name").get(0).href = '/user/' + rel['_uid'];
            if (rel['user']) info.children('.user-ops').show()
            // 显示在界面上的信息处理
            if (rel['chat-count']) {// 聊天室未读信息
                $('.bar-chat').append('<div class="after" data-count="' +
                    (rel['chat-count'] > 99 ? '99+' : rel['chat-count'])
                    + '" >');
            }
            user_data = rel;
            if (afterdata) afterdata();
        }
    }).fail(function () {
        $.cookie('_uid', '', {
            path: '/'
        });
    });
    $('.open-nav').bind('click', function () {
        $('.nav').show().animate({
            'left': '0'
        });
        $('.layout').show().animate({
            'opacity': '1'
        });
    });
    $('.layout').bind('click', function () {
        $('.nav').animate({
            'left': '-100%'
        });
        $('.layout').animate({
            'opacity': '0'
        }, function () {
            $('.layout').hide();
        });
    });
});
