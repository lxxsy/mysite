$(function() {
    // 提交评论触发
    $('#comment-form').submit(function(){
        // 判断评论内容是否为空
        $('#comment_error').text('');
        if (CKEDITOR.instances['id_text'].document.getBody().getText().trim()==''){
            $('#comment_error').text('评论内容不能为空');
            return false;
        };
        // 富文本编辑器配置
        CKEDITOR.instances['id_text'].updateElement();
        $.ajax({
            url: '/comment/',
            type: "POST",
            data: $(this).serialize(),
            success: function(data){
                if (data['status']=='SUCCESS'){
                    if ($('#id_reply_comment_pk').val()==0){
                        // 插入评论
                        var comment_html = '<div class="comment" id="'+data["pk"]+'">'
                                        +'<span>'+data["username"]+'</span>'
                                        +'<span>'+'('+data["comment_time"]+')</span>'
                                        +'<span class="comment-text">'+data["text"]+'</span>'
                                        +'<button class="btn btn-primary reply_pk">回复</button>'
                                        +'</div>';
                        $('#comment_list').prepend(comment_html);
                    }else{
                        // 插入回复
                        var reply_html = '<div class="reply", id="'+data["pk"]+'">'
                                    +'<span>'+data["username"]+'</span>'
                                    +'<span>'+'('+data["comment_time"]+')</span>'
                                    +'<span>回复</span>'
                                    +'<span>'+data["reply_to"]+':</span>'
                                    +'<span class="reply-text">'+data["text"]+'</span>'
                                    +'<button class="btn btn-primary reply_pk">回复</button>'
                                    +'</div>';
                        $("#"+data['root_pk']).append(reply_html);
                    };
                    // 清空编辑框的内容
                    CKEDITOR.instances['id_text'].setData('');
                    $('#comment_error').text('评论成功');
                }else{
                    $('#comment_error').text(data['message']);
                };
            },
            error: function(xhr){
                console.log(xhr);
            }
        })
        return false;
    });

    // 点击回复按钮
    $('.comment').on('click', '.reply_pk', function(){
        var reply_button_this = $(this);
        reply(reply_button_this);
    });

    // 点击点赞图标，事件捕捉,【废弃】
    $('.like').click(function(){
        if (obj.find('span').eq(1).text()==0){
            obj.find('span').eq(1).text(1);
            obj.find('span').eq(0).addClass('active');   
        }else{
            obj.find('span').eq(1).text(0);
            obj.find('span').eq(0).removeClass('active');    
        };
        like(content_type, object_id, judge);
    });

    // 评论被回复，执行此函数
    function reply(reply_button_this){
        $('#reply_content_container').show();
        $('#id_reply_comment_pk').val(reply_button_this.parent().attr('id'));
        $('html').animate({scrollTop: $('#comment-form').offset().top - 60}, 300, function(){
            CKEDITOR.instances['id_text'].focus();
        });
        $('#reply_content').html('<p>'+ reply_button_this.prev().html()+'</p>');
    };

    // 点赞逻辑处理函数，【废弃】
    function like(content_type, object_id, judge){
        $.ajax({
            url: "/likes/",
            type: "GET",
            data: {
                'content_type': content_type,
                'object_id': object_id,
                'judge': judge
            },
            cache: false,
            success: function(data){

            },
            error: function(data){

            }
        })
    };
});