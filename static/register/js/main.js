code_interval = null, countdown = 60;
check_state = {
    'user': false,
    'pwd1': false,
    'pwd2': false,
    'mail': false,
    'code': false
};

function is_mail(mail) {
    if (!mail) return false;
    var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    isok = reg.test(mail);
    if (!isok) {
        return false;
    }
    return true;
}

function clear_state(e) { e.removeClass('checking').removeClass('wrong').removeClass('right') }
function state_wrong(e) { clear_state(e), e.addClass('wrong'); }
function state_right(e) { clear_state(e), e.addClass('right'); }
function state_waiting(e) { clear_state(e), e.addClass('waiting'); }

function check_user() {
    var user = $('#user input').val();
    var state = $('#user .input-state').addClass('checking');
    check_state['user'] = false;
    if (!user) {
        check_state['user'] = false;
        state_wrong(state);
    } else
        $.post('/api/has/user', {
            'user': user
        }, function (rel) {
            if (rel == 'True') {
                check_state['user'] = false;
                state_wrong(state);
            } else if (rel == 'False') {
                check_state['user'] = true;
                state_right(state);
                check_all();
            }
        }).fail(function () {
            check_state['user'] = false;
            state_wrong(state);
        });
}

function check_pwd1() {
    var state = $('#pwd1 .input-state').addClass('checking');
    var pwd1 = $('#pwd1 input').val();
    if (!pwd1 || pwd1.length < 8) {
        check_state['pwd1'] = false;
        state_wrong(state);
    } else {
        check_state['pwd1'] = true;
        state_right(state);
        check_all();
    }
    if ($('#pwd2 input').val() != '')
        check_pwd2();
}
function check_pwd2() {
    var state = $('#pwd2 .input-state').addClass('checking');
    var pwd1 = $('#pwd1 input').val();
    var pwd2 = $('#pwd2 input').val();
    if (!pwd2 || pwd1 != pwd2 || pwd1.length < 8) {
        check_state['pwd2'] = false;
        state_wrong(state);
    } else {
        check_state['pwd2'] = true;
        state_right(state);
        check_all();
    }
}

function check_mail() {
    var mail = $('#mail input').val();
    var state = $('#mail .input-state').addClass('checking');
    if (!mail || !is_mail(mail)) {
        check_state['mail'] = false;
        state_wrong(state);
    } else {
        check_state['mail'] = true;
        state_right(state);
        check_all();
    }
    if ($('#code input').val() != '') check_code();
}



function get_code() {
    check_mail();
    if (!check_state['mail']) return;
    $.post('/register/code', {
        'mail': $('#mail input').val()
    }, function (rel) {
        if (rel['code'] == 0) {
            $('#code .get').attr('disabled', 'disabled');
            countdown = 60;
            code_interval = setInterval(function () {
                countdown -= 1;
                $('#code .get').val('重新获取('+countdown+')');
                if(countdown <= 0){
                    clearInterval(code_interval);
                    $('#code .get').val('重新获取').removeAttr('disabled');
                }
            }, 1000);
        } else {

        }
    });
}

function check_code() {
    var mail = $('#mail input').val();
    var code = $('#code input').val();
    var state = $('#code .input-state').addClass('checking');
    check_state['code'] = false;
    if (!code || !mail) {
        check_state['code'] = false;
        state_wrong(state);
    } else
        $.post('/register/code/check', {
            'mail': mail,
            'code': code
        }, function (rel) {
            if (rel == 'False') {
                check_state['code'] = false;
                state_wrong(state);
            } else if (rel == 'True') {
                check_state['code'] = true;
                state_right(state);
                check_all();
            }
        }).fail(function () {
            check_state['code'] = false;
            state_wrong(state);
        });
}

function check_all() {
    for (var i in check_state) {
        if (!check_state[i]) {
            $('.submit').attr('disabled', 'disabled');
            return;
        }
    }
    $('.submit').removeAttr('disabled');
}

$(document).ready(function () {
    $(document) //
        .on('input', '#user input', check_user)
        .on('input', '#pwd1 input', check_pwd1)
        .on('input', '#pwd2 input', check_pwd2)
        .on('input', '#mail input', check_mail)
        .on('input', '#code input', check_code)
        .on('click', '#code .get', get_code)
});