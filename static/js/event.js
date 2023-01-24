function get_randint() {
    $.ajax({
        type: 'GET',
        url: '/randint',
        data: {},
        success: function (response) {
            $('#luckyBoxTitle').empty()
            $('#luckyBoxBody').empty()
            let lucky_num = response["lucky_num"]
            let lucky_title = "축하합니다"
            let lucky_body = `<img class="card-img-top" src="/static/success.png" style="width:250px; height:250px;" alt="광고">`
            // <br>
            // <br>
            // 스타벅스 기프티콘 당첨되셨어요.`
            let unlucky_title = "아쉽군요"
            let unlucky_body = `<img class="card-img-top" src="/static/fail.png" style="width:250px; height:250px;" alt="광고">`
            // <br>
            // <br>
            // 꽝입니다.`
            if (lucky_num == 1) {
                $('#luckyBoxTitle').append(lucky_title)
                $('#luckyBoxBody').append(lucky_body)
            } else {
                $('#luckyBoxTitle').append(unlucky_title)
                $('#luckyBoxBody').append(unlucky_body)
            }
        }
    });
}

function get_fortune() {
    $.ajax({
        type: 'GET',
        url: '/fortune',
        data: {},
        success: function (response) {
            $('#fortuneBoxBody').empty()
            let fortune_body = response["fortune"]
            $('#fortuneBoxBody').append(fortune_body)
        }
    });
}