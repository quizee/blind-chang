function changeModal(post_id) {
    //alert(post_id)
    $.ajax({
        type: 'GET',
        url: `/blind/one-post?post_id=${post_id}`,
        data: {},
        success: function (response) {
            $('#comment_list').empty();
            let post_author = response['nick_name']
            let content = response['content']
            let title = response['title']

            $('#post-title-modal').text(title);
            $('#post-author-modal').text(post_author);
            $('#post-content-modal').text(content);
            $('#postModal').data('current-post', post_id)


            let comments = response['comments'];
            for (let i = 0; i < comments.length; i++) {
                let comment_author = comments[i]['nick_name']
                let comment = comments[i]['comment']
                let comment_html = `
                        <li class="list-group-item d-flex justify-content-between">
                                <div class="ms-2 me-auto">
                                    <small class="text-muted">${comment_author}</small>
                                    <div>${comment}</div>
                                </div>
                            </li>
                        `
                $('#comment_list').append(comment_html)
            }
        }
    })
}

function range(start, stop) {
    var a = [start], b = start;
    while (b < stop) {
        a.push(b += 1);
    }
    return a;
}

function show_acc() {
    $.ajax({
        type: "GET",
        url: `/blind/acc`,
        data: {},
        success: function (response) {
            let total_views = response['total_views']
            $('#acc_num').text(total_views)
        }

    })
}

function show_post(page_num) {
    $.ajax({
        type: "GET",
        url: `/blind?page=${page_num}`,
        data: {},
        success: function (response) {
            let username = response['username']
            if (username !== "") {
                $('#name').val(username);
                $('#nickname-form').val(username);
                //$("#name").attr("disabled", true);
            }

            $('#post-list').empty();
            $('#button-list').empty();
            $('#popular_list').empty();
            let popular_posts = response['popular_posts']
            let rows = response['posts']

            let current_page = page_num;
            let total_pages = Math.ceil(response['post_num'] / 5);
            let window = 3

            let start = current_page - window
            let end = current_page + window

            if (start <= 0) {
                end = end - start + 1;
                start = 1;
            }
            if (end > total_pages) {
                end = total_pages;
                start = Math.max(end - (window * 2) + 1, 1)
            }

            let buttons = range(start, end)
            console.log(buttons)

            let previous_disabled = ""
            let next_disabled = ""
            console.log(total_pages, page_num)

            if (current_page === 1) {
                previous_disabled = "disabled"
            }
            if (current_page === total_pages) {
                next_disabled = "disabled"
            }
            let first_button = `
                        <li class="page-item ${previous_disabled}"><a class="page-link" href="javascript:show_post(${current_page - 1})" tabindex="-1"><</a>
                    </li>`

            let last_button = `
                        <li class="page-item ${next_disabled}"><a class="page-link" href="javascript:show_post(${current_page + 1})" tabindex="-1">></a>
                    </li>
                    `
            $('#button-list').append(first_button)
            // 앞부분
            for (let i = 0; i < buttons.length; i++) {
                let button_num = buttons[i]
                let active = ""
                if (button_num === current_page) {
                    active = "active"
                }
                let button_html = `
                            <li class="page-item ${active}"><a class="page-link" href="javascript:show_post(${button_num})">${button_num}</a></li>
                        `
                $('#button-list').append(button_html)
            }
            $('#button-list').append(last_button)
            // paging 끝
            // 테스트입니다. 기능 추가했습니다

            // 실시간 인기 post 나열
            for (let i = 0; i < popular_posts.length; i++) {
                let title = popular_posts[i]['title'];
                let comments = popular_posts[i]['comments'];
                let post_id = popular_posts[i]['post_id'];
                let temp_html = `
                            <li class="list-group-item d-flex justify-content-between align-items-start" data-bs-toggle="modal" data-bs-target="#postModal" onclick="changeModal(${post_id})">
                                <div class="ms-2 me-auto text-truncate">
                                    ${title}
                                </div>
                                <span class="badge bg-primary rounded-pill">${comments}</span>
                            </li>
                        `
                $('#popular_list').append(temp_html)
            }


            // post 나열
            for (let i = 0; i < rows.length; i++) {
                let nick_name = rows[i]['nick_name'];
                let content = rows[i]['content'];
                let title = rows[i]['title']
                let post_id = rows[i]['post_id']
                let views = rows[i]['views']
                let comments = rows[i]['comments']
                console.log(nick_name, content, title)
                let temp_html = `
                        <div class="card" data-bs-toggle="modal" data-bs-target="#postModal" onclick="changeModal(${post_id})">
                            <div class="card-body">
                               <p><small class="text-muted">no. ${post_id} </small></p>
                               <p class="card-text"><small class="text-muted">${nick_name}</small></p>
                              <h5 class="card-title text-truncate" style="max-width: 330px;">${title}</h5>
                              <span class="card-text d-inline-block text-truncate" style="max-width: 330px;">${content}</span>
                            </div>
                            <div class="card-footer">
                              <div class="container">
                              <div class="row">
                              <div class="col-md-8 d-flex justify-content-center">

                                </div>
                                <div class="col-md-2 d-flex justify-content-center">
                                <i class="fa-regular fa-comment"><small class="text-muted"> ${comments} </small></i>
                                </div>
                                <div class="col-md-2 d-flex justify-content-center">
                                <i class="fa fa-eye"><small class="text-muted"> ${views} </small></i>
                                </div>
                                </div>
                                </div>
                            </div>
                        </div>`
                $('#post-list').append(temp_html);
            }
        }
    });
}