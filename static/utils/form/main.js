function input_click(d) {
    d.animate({
        'font-size': '16px',
        'left': '0',
        'top': '-10px',
        'height': '20px',
        'line-height': '20px',
        'padding-left': '5px',
    }, 100);
}
function password_show(e) {
    $(this).addClass('select');
    $(this).siblings('input').attr('type', 'text');
}
function password_hide(e) {
    $(this).removeClass('select');
    $(this).siblings('input').attr('type', 'password');
}


$(document).ready(function () {
    $('.form .input').on('click', '.input-title', function () {
        $(this).siblings('input').focus();
    });
    $('.form .input').on('focus', 'input', function () {
        input_click($(this).siblings('.input-title'));
    });
    $('.form .input').on('blur', 'input', function () {
        if (this.value.length == 0) {
            var d = $(this).siblings('.input-title');
            d.animate({
                'font-size': '20px',
                'top': '0px',
                'height': '100%',
                'line-height': '40px',
                'padding-left': '5%',
            }, 100);
        }
    });
    $('.form .input-password')
        .on('mousedown', '.show', password_show)
        .on('touchstart', '.show', password_show)
        .on('mouseup', '.show', password_hide)
        .on('mouseout', '.show', password_hide)
        .on('touchend', '.show', password_hide)
        .on('contextmenu', function (e) { e.preventDefault(); })


    $('.form .input').each(function () {
        if (this.getAttribute('data-text')) {
            title = document.createElement('span');
            title.className = 'input-title';
            title.setAttribute('data-text', this.getAttribute('data-text'));
            $(this).append(title);
        }
        state = document.createElement('span');
        state.className = 'input-state';
        $(this).append(state);
    });
    $('.form .input-text').each(function () {
        input = document.createElement('input');
        input.type = 'text';
        input.name = this.getAttribute('data-name');
        input.value = this.getAttribute('data-value') || '';
        $(this).append(input);
        if (this.getAttribute('data-value'))
            $(this).children('span').trigger('click');
    });
    $('.form .input-password').each(function () {
        input = document.createElement('input');
        input.type = 'password';
        input.name = this.getAttribute('data-name');
        show = document.createElement('em');
        show.className = 'show';
        $(this).append(show);
        $(this).append(input);
    });
    $('.form .input.verify').each(function () {
        input = document.createElement('input');
        input.type = 'tel';
        input.name = this.getAttribute('data-name');
        input.maxLength = "6";
        get = document.createElement('input');
        get.className = 'get';
        get.type = 'button';
        get.setAttribute('onclick', this.getAttribute('data-action'));
        get.value = '获取验证码';
        $(this).append(input);
        $(this).append(get);
    });
    $('.form div.submit').each(function () {
        input = document.createElement('input');
        input.type = 'submit';
        input.value = this.getAttribute('data-text');
        $(this).append(input);
    });
});


function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return decodeURI(r[2]); return null; //返回参数值
}