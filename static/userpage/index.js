document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {

        // --------------------------------
        // Posts Paginator
        // --------------------------------

        let page = 2

        function bottomScroll() {
            if ($(window).scrollTop() + $(window).height() == $(document).height()) {
                document.querySelector('#loading').innerHTML = `<div class="spinner-border text-primary" role="status">
                <span class="sr-only">Loading...</span>
              </div>`
                $.ajax({
                    url: window.location.pathname,
                    data: {
                        'page': page
                    },
                    method: 'get',
                    dataType: 'json',
                    async: false,
                    success: function (response) {
                        page++
                        posts = JSON.parse(response.posts)
                        if (posts.length > 0) {
                            for (post of posts) {
                                $.ajax({
                                    url: $('#posts').attr('data-url'), // {% url 'get_user_by_id' %}
                                    data: {
                                        'pk': post.fields.user,
                                    },
                                    method: 'get',
                                    dataType: 'json',
                                    async: false,
                                    success: function (response) {
                                        let user = response.user
                                        let output = ''
                                        let postCategory = 'other'
                                        if (post.fields.category) {
                                            postCategory = post.fields.category
                                        }
                                        let dateToString = d =>
                                            `${d.getFullYear()}-${('00' + (d.getMonth() + 1)).slice(-2)}-${('00' + d.getDate()).slice(-2)}`
                                        let postDate = new Date(Date.parse(post.fields.post_date))
                                        let date = dateToString(postDate)
                                        output = `

                                    <div class="card gedf-card">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="mr-2">
                                    <a href="/people/${user.id}" target='_blank'>
                                        <img src="${user.avatar}" alt = ""width="45" class="rounded-circle"
                                            loading="lazy">
                                    </a>
                                </div>
                                <div class="ml-2">
                                    <div class="h5 m-0">${user.username}</div>
                                    <div class="h7 text-muted">${post.fields.views.length} Views -
                                        ${postCategory}
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="card-body">
                        <div class="text-muted h7 mb-2"> <i class="fa fa-clock-o"></i>${date}</div>
                        <!-- Title -->
                        <p class="card-link btn-link" href="#">
                            <h5 class="card-title postDescription">${post.fields.description.substring(0, 45)}</h5>
                        </p>
                                    `
                                        // Image
                                        if (post.fields.image) {
                                            output += `<img src="/media/${post.fields.image}" alt="" style="width:80%; height: auto; margin-left: auto; margin-right: auto;">`
                                        }
                                        // Video
                                        if (post.fields.post_file) {
                                            output += `
                                        <video controls class="col-md-10 col-lg-8" preload="none">
                            <source src="/media/${post.fields.post_file}" type="video/mp4">
                            <source src="/media/${post.fields.post_file}" type="video/ogg">
                            Your browser does not support the video tag.
                        </video>
                                    `
                                        }
                                        // Description
                                        if (post.fields.description.length > 45) {
                                            let readMore = '';
                                            if (post.fields.description.length > 227) {
                                                readMore = `<a href="#" class="readMore">Read more</a>`;
                                            };
                                            output += `
                                        <p class="card-text postDescription" style="white-space: pre-line;">
                            ${post.fields.description.substring(0, 227)} ${readMore}
                        </p>
                                    `
                                        };

                                        output += `
                                    </div>
                    <div class="card-footer">
                        <form method="GET" class="likeForm d-inline"
                            action="/comments/post_like_dislike/${post.pk}/" data-pk="${post.pk}">
                            <button type="submit" class="btn"><i class="far fa-thumbs-up"></i>
                                <span id="id_likes${post.pk}">
                                    <p style="color:black;display: inline">${post.fields.likes.length}</p>
                                </span>
                                Like</button>
                        </form>
                        <form action="/comments/post_like_dislike/${post.pk}/" method="GET"
                            class="d-inline dislikeForm" data-pk="${post.pk}">
                            <button type="submit" class="btn"><i class="far fa-thumbs-down"></i>
                                <span id="id_dislikes${post.pk}">
                                    <p style="color:black; display: inline;">${post.fields.dislikes.length}</p>
                                </span>
                                Dislike
                            </button>
                        </form>
                        <a href="/comments/${post.pk}/" class="card-link"><i
                                class="fab fa-rocketchat"></i>
                            Comments</a>
                        <!-- AddToAny BEGIN -->
                        <a href="https://www.addtoany.com/share#url=https%3A%2F%2Fwww.dfreemedia.com/commetns/${post.pk}&amp;title=${post.fields.description.substring(0, 45)}"
                            target="_blank" class="card-link"><i class="fa fa-mail-forward"></i> Share</a>
                        <!-- AddToAny END -->
                    </div>
                </div>
                                `
                                        $('#posts').append(output)

                                        function showMore() {
                                            $('.readMore').click(function (e) {
                                                e.preventDefault();
                                                $(this).parent().html(`<br> ${post.fields.description}`)
                                            })
                                        }
                                        let g = document.createElement('script');
                                        let s = document.getElementsByTagName('script')[0]
                                        g.text = showMore();
                                        s.parentNode.insertBefore(g, s)
                                    }
                                })
                            }
                        } else {
                            document.querySelector('#loading').innerHTML = ''
                        }
                    }
                })
            }
        }
        bottomScroll();
        $(window).scroll((e) => {
            bottomScroll()
        })


        // --------------------------------
        // Navigate edit profile
        // --------------------------------
        $('.editForm').hide()
        $('#personalForm').show()
        $('#editNavbar ul li').click(function (e) {
            e.preventDefault()
            $('.editForm').hide()
            if ($(this).html().includes('Personal')) {
                $('#personalForm').show()
            } else if ($(this).html().includes('Distraction Free')) {
                $('#distractionFreeForm').show()
            } else if ($(this).html().includes('Privacy')) {
                $('#privacyForm').show()
            } else {
                $('#advanceForm').show()
            }
        })

        // --------------------------------
        // Like
        // --------------------------------
        $('.likeForm').submit(function (e) {
            e.preventDefault();
            let thisElement = $(this)
            $.ajax({
                url: thisElement.attr('action'),
                data: {
                    'submit': 'like',
                },
                dataType: 'json',
                method: 'get',
                async: false, // Have a look into this
                success: function (response) {
                    let likes = $(`#id_likes${thisElement.attr('data-pk')}`).find('p').html()
                    let dislikes = $(`#id_dislikes${thisElement.attr('data-pk')}`).find('p').html()
                    if (response.action == 'undislike_and_like') {
                        dislikes -= 1
                        likes++
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${likes}</p>`)
                    } else if (response.action == 'unlike') {
                        likes -= 1
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${likes}</p>`)
                    } else { //Like only
                        likes++
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${likes}</p>`)
                    }
                }
            })
        })
        // Dislike
        $('.dislikeForm').submit(function (e) {
            e.preventDefault();
            let thisElement = $(this)
            $.ajax({
                url: thisElement.attr('action'),
                data: {
                    'submit': 'dislike',
                },
                dataType: 'json',
                method: 'get',
                async: false,
                success: function (response) {
                    let likes = $(`#id_likes${thisElement.attr('data-pk')}`).find('p').html()
                    let dislikes = $(`#id_dislikes${thisElement.attr('data-pk')}`).find('p').html()
                    if (response.action == 'unlike_and_dislike') {
                        dislikes++
                        likes -= 1
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${likes}</p>`)
                    } else if (response.action === 'undislike') {
                        dislikes -= 1
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black; display: inline;">${dislikes}</p>`)
                    } else {
                        dislikes++
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline;">${dislikes}</p>`)
                    }
                }
            })
        })

        // ---------------
        // Display text
        // ---------------
        $('#id_avatar').change(function() {
            console.log('Changed')
            var i = $(this).prev('label').clone();
            var file = $('#id_avatar')[0].files[0].name;
            $(this).prev('label').text(file);
          });
        $('#id_cover').change(function() {
            console.log('Changed')
            var i = $(this).prev('label').clone();
            var file = $('#id_cover')[0].files[0].name;
            $(this).prev('label').text(file);
          });
    })
})