function save_post() {
    let nick_name = $('#name').val();
    let content = $('#content').val();
    let title = $('#post_title').val();
    if (content === "") {
        alert("내용칸이 비어있네요!😮 어떤 얘기도 좋아요 ")
        return
    }
    if (nick_name === "") {
        alert("닉네임을 작성해주세요! 익명보장되니깐요 😉")
        return
    }

    if (title === "") {
        alert("제목을 깜빡하신 것 같습니다 대표님😎")
        return
    }

    $.ajax({
        type: 'POST',
        url: '/blind',
        data: {
            nick_name: nick_name,
            content: content,
            title: title
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

function save_comment() {
    let comment = $('#comment-form').val();
    let current_post_id = $('#postModal').data('current-post');
    let nickname = $('#nickname-form').val();
    if (comment === "") {
        alert("댓글칸이 비어있네요 대표님!")
        return
    }
    if (nickname === "") {
        alert("닉네임칸이 비어있네요 대표님!")
        return
    }
    $.ajax({
        type: 'POST',
        url: '/blind/comment',
        data: {
            comment: comment,
            post_id: current_post_id,
            nick_name: nickname
        },
        success: function (response) {
            //alert(response['msg']);
            $('#comment-form').val("");
            changeModal(current_post_id);
        }
    });
}