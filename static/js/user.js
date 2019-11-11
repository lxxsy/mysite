$(function(){
    $('#code').click(function(){
        var email = $('#id_email').val();
        if (email == ''){
            $('#tip').text('*邮箱不能为空');
            return false;
        }
        // 发送验证码
        $.ajax({
            url: '/user/send_verification_code/',
            type: 'GET',
            data: {'email': email},
            cache: false,
            success: function(data){
                if (data['status'] == 'ERROR'){
                    alert(data['status']);
                }
            }
        })
        // 把按钮变灰，再次发送验证码需60秒
        $(this).addClass('disabled');
        $(this).attr('disabled', true);
        var time = 60;
        $(this).text(time + 's');
        var interval = setInterval(() => {
            if (time <= 0){
                clearInterval(interval);
                $(this).removeClass('disabled');
                $(this).attr('disabled', false);
                $(this).text('发送验证码');
                return false;
            }
            time --;
            $(this).text(time + 's');
        }, 1000)
    });
});