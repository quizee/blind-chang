var count = -1;

function get_randint() {
    $.ajax({
        type: 'GET',
        url: '/randint',
        data: {},
        success: function (response) {
            count = count + 1;
            $('#luckyBoxTitle').empty()
            $('#luckyBoxemoji').empty()
            $('#luckyBoxBody').empty()
            let lucky_num = response["lucky_num"]
            let lucky_title = "당신은 럭키 그 잡채"
            let lucky_emoji = "🎉"
            let lucky_body = "<strong>"+count+"</strong>번째 시도에 성공<br><br>지금 화면을 캡쳐해서 Slack 잡담방에 올려주세요.<br>스타벅스 기프티콘을 드리겠습니다."
            let unlucky_title = "당신은 실패한 것이 아닙니다.<br>도전할 수 있는 기회가 더 주어진 것일뿐"
            let unlucky_emoji = "🔥"
            let unlucky_body = "스타벅스 기프티콘으로 향하는 <strong>"+count+"</strong>번째 시도"
            if (lucky_num == 1) {
                $('#luckyBoxTitle').append(lucky_title)
                $('#luckyBoxemoji').append(lucky_emoji)
                $('#luckyBoxBody').append(lucky_body)
                return count
            } else {
                $('#luckyBoxTitle').append(unlucky_title)
                $('#luckyBoxemoji').append(unlucky_emoji)
                $('#luckyBoxBody').append(unlucky_body)
                return count
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