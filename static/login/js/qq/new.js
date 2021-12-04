tip = null;

$(document).ready(function () {
    tip = document.getElementsByClassName('tip')[0]
    $('#user').on('blur', 'input', function () {
        tip.innerHTML = '';
        $('.submit').attr('disabled', 'disabled');
        if (this.value.length === 0) {
            tip.innerHTML = '<i class="fas fa-times"></i>' + '用户名不可为空';
            return;
        }
        $.post('/api/hasuser', { 'user': this.value }, function (rel) {
            if (rel == 'False') {
                tip.innerHTML = '<i class="fas fa-times"></i>' + '该用户名已存在';
            }else{
                $('.submit').removeAttr('disabled');
            }
        }).fail(function(){
            tip.innerHTML = '<i class="fas fa-times"></i>' + '请求错误';
        })
    });
});