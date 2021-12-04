$(document).ready(function () {

    $('#qqLoginBtn').click(function () {
        window.location.href = 'https://graph.qq.com/oauth2.0/authorize?display=mobile&response_type=code&client_id=101978697&redirect_uri=https%3A%2F%2Fsakuyark.com%2Flogin%2Fqq&state=login'
    });
});