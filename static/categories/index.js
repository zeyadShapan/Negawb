document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('load', function () {
        let homepage_post_page = 2
        let followed_post_page = 2
        $('.homepageItem').hide()
        $('#postsContainer').show()
        $('.homepageView').click(function (e) {
            e.preventDefault();
            if (!$(this).hasClass('active')) {
                $('.homepageView').removeClass('active')
                $(this).addClass('active')
                $('.homepageItem').hide()
                if ($(this).html() === 'Topics') {
                    $('#categoryContainer').show()
                } else if ($(this).html() === 'Posts') {
                    $('#postsContainer').show()
                } else if ($(this).html() == 'Followed') {
                    $('#followedPosts').show()
                }
            }
        })


        function bottomScroll() {
            // homepage posts
            if ($(window).scrollTop() + $(window).height() == $(document).height() && $('.homepageView.active').html() == 'Posts') {
                $.ajax({
                    url: '',
                    data: {
                        'homepage_posts_page': homepage_post_page
                    },
                    method: 'get',
                    dataType: 'json',
                    async: false,
                    success: function (response) {
                        homepage_post_page++
                        posts = JSON.parse(response.homepage_posts)
                        for (post of posts) {
                            let output = ''
                            $.ajax({
                                url: $('#categoryContainer').attr('data-url'),
                                data: {
                                    'pk': post.fields.user,
                                },
                                method: 'get',
                                dataType: 'json',
                                async: false,
                                success: function (response) {
                                    let user = response.user
                                    let output = ''
                                    let userAvatar = ''
                                    if (user.who_see_avatar == 'everyone') {
                                        userAvatar = user.avatar
                                    } else if (user.who_see_avatar == 'friends' && $('#categoryContainer').attr('data-currUser') in JSON.parse(user.friends)) {
                                        userAvatar = user.avatar
                                    } else if ($('#categoryContainer').attr('data-currUser') == user) {
                                        userAvatar = user.avatar
                                    } else {
                                        userAvatar = `/media/profile_images/DefaultUserImage.jpg`
                                    }
                                    output = `
                                    <a href="/people/${user.id}">
        <img src="${userAvatar}" alt="${user.username }" width="64" height="64"
            class="mr-3 float-left rounded-circle" loading="lazy">
            <span>${user.username}</span>
    </a>
    <div class="mb-3">
        <div class="card-body">
                                    `
                                    if (post.fields.description) {
                                        let readMore = ''
                                        if (post.fields.description.length > 450) {
                                            readMore = `<a href="/comments/${post.pk}/">Read More</a>`
                                        }
                                        output += `
                                        <blockquote class="blockquote mb-0">
                <p class="text-break" style="white-space: pre-wrap;">${post.fields.description.substring(0,450)} ${readMore}</p>
            </blockquote>
                                    `
                                    }
                                    output += `<small class="form-text text-muted">${post.fields.views.length} Views ♦︎ ${ post.fields.post_date }</small>`
                                    if (post.fields.image) {
                                        output += `<img src="/media/${ post.fields.image }" alt="${ user.username }" height="250" width="40%">                                    `
                                    }
                                    if (post.fields.post_file) {
                                        output += `
                                        <video width="100%" controls class="col-md-10 col-lg-8" preload="none">
                <source src="${ post.fields.post_file }" type="video/mp4">
                <source src="/media/${ post.fields.post_file }" type="video/ogg">
                Your browser does not support the video tag.
            </video>
                                    `
                                    }
                                    output += `
                                    </div>
                                </div>
                                <span class="row justify-content-center">
    <span><a href="/comments/${post.pk}/" style="text-decoration: none; color:black;"><i
                class="far fa-comment-dots" style="font-size:36px;"></i></a></span>
    <!-- Like -->
    <form action="/comments/post_like_dislike/${post.pk}/" method="GET" class="form-inline likeForm" data-pk="${post.pk}">
        <button type="submit" name="submit" value="like" title="Like" class="btn btn-link">
            <i class="fa fa-thumbs-o-up" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_likes${post.pk}">
        <p style="color:black;">${post.fields.likes.length}</p>
        </span>
        <!-- Dislike -->
        <form action="/comments/post_like_dislike/${post.pk}/" method="GET" class="form-inline dislikeForm" data-pk="${post.pk}">
        <button type="submit" name="submit" value="dislike" title="Dislike" class="btn">
            <i class="fa fa-thumbs-o-down" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_dislikes${post.pk}">
        <p style="color:black;">${post.fields.dislikes.length}</p>
        </span>
                                `
                                    $('#postsContainer').append(output)
                                }
                            })
                        }
                    }
                })
                // Follwed posts
            } else if ($(window).scrollTop() + $(window).height() == $(document).height() && $('.homepageView.active').html() == 'Followed') {
                $.ajax({
                    url: '',
                    data: {
                        'followed_page': followed_post_page,
                    },
                    method: 'get',
                    dataType: 'json',
                    async: false,
                    success: function (response) {
                        followed_post_page++
                        posts = JSON.parse(response.followed_posts)
                        for (post of posts) {
                            let output = ''
                            $.ajax({
                                url: $('#categoryContainer').attr('data-url'),
                                data: {
                                    'pk': post.fields.user,
                                },
                                method: 'get',
                                dataType: 'json',
                                async: false,
                                success: function (response) {
                                    let user = response.user
                                    let output = ''
                                    let userAvatar = ''
                                    if (user.who_see_avatar == 'everyone') {
                                        userAvatar = user.avatar
                                    } else if (user.who_see_avatar == 'friends' && $('#categoryContainer').attr('data-currUser') in JSON.parse(user.friends)) {
                                        userAvatar = user.avatar
                                    } else if ($('#categoryContainer').attr('data-currUser') == user) {
                                        userAvatar = user.avatar
                                    } else {
                                        userAvatar = `/media/profile_images/DefaultUserImage.jpg`
                                    }
                                    output = `
                                    <a href="/people/${user.id}">
        <img src="${userAvatar}" alt="${user.username }" width="64" height="64"
            class="mr-3 float-left rounded-circle" loading="lazy">
            <span>${user.username}</span>
    </a>
    <div class="mb-3">
        <div class="card-body">
                                    `
                                    if (post.fields.description) {
                                        let readMore = ''
                                        if (post.fields.description.length > 450) {
                                            readMore = `<a href="/comments/${post.pk}/">Read More</a>`
                                        }
                                        output += `
                                        <blockquote class="blockquote mb-0">
                <p class="text-break" style="white-space: pre-wrap;">${post.fields.description.substring(0, 450)} ${readMore}</p>
            </blockquote>
                                    `
                                    }
                                    output += `<small class="form-text text-muted">${post.fields.views.length} Views ♦︎ ${ post.fields.post_date }</small>`
                                    if (post.fields.image) {
                                        output += `<img src="/media/${ post.fields.image }" alt="${ user.username }" height="250" width="40%">                                    `
                                    }
                                    if (post.fields.post_file) {
                                        output += `
                                        <video width="100%" controls class="col-md-10 col-lg-8" preload="none">
                <source src="${ post.fields.post_file }" type="video/mp4">
                <source src="/media/${ post.fields.post_file }" type="video/ogg">
                Your browser does not support the video tag.
            </video>
                                    `
                                    }
                                    output += `
                                    </div>
                                </div>
                                <span class="row justify-content-center">
    <span><a href="/comments/${post.pk}" style="text-decoration: none; color:black;"><i
                class="far fa-comment-dots" style="font-size:36px;"></i></a></span>
    <!-- Like -->
    <form method="GET" class="likeForm" class="form-inline" data-pk="${post.pk}">
        <button type="submit" name="submit" value="like" title="Like" class="btn btn-link">
            <i class="fa fa-thumbs-o-up" aria-hidden="true" style="font-size:36px" id="likeButton${post.pk}"></i>
        </button>
    </form>
    <span class="m-3" id="id_likes${post.pk}">
        <p style="color:black;">${post.fields.likes.length}</p>
        </span>
        <!-- Dislike -->
        <form action="/comments/${post.pk}" method="post" class="form-inline"
        id="dislikeForm${post.pk}">
        <button type="submit" name="submit" value="dislike" title="Dislike" class="btn">
            <i class="fa fa-thumbs-o-down" aria-hidden="true" style="font-size:36px"></i>
        </button>
    </form>
    <span class="m-3" id="id_dislikes${post.pk}">
        <p style="color:#065FD4;"><b>${post.fields.dislikes.length}</b></p>
        </span>
                                `
                                    $('#followedPostsContainer').append(output)

                                }
                            })
                        }
                    }
                })
            }
        }
        bottomScroll();
        $(window).scroll((e) => {
            bottomScroll()
        })
        // Like
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
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4; display: inline">${likes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${dislikes}</p>`)
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${likes}</p>`)
                    } else if (response.action == 'unlike') {
                        likes -= 1
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${likes}</p>`)
                        // Followed
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${likes}</p>`)
                    } else { //Like only
                        likes++
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${likes}</p>`)
                        // Followed
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${likes}</p>`)
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
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${dislikes}</p>`)
                        $(`#id_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${likes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${dislikes}</p>`)
                        $(`#followed_likes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${likes}</p>`)
                    } else if (response.action === 'undislike') {
                        dislikes -= 1
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${dislikes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:black;display: inline">${dislikes}</p>`)
                    } else {
                        dislikes++
                        $(`#id_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${dislikes}</p>`)
                        // Followed
                        $(`#followed_dislikes${thisElement.attr('data-pk')}`).html(`<p style="color:#065FD4;display: inline">${dislikes}</p>`)
                    }
                }
            })
        })
        $('#image').change(function (e) {
            for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
                var file = e.originalEvent.srcElement.files[i];
                var img = document.createElement("img");
                var reader = new FileReader();
                reader.onloadend = function () {
                    img.src = reader.result;
                }
                reader.readAsDataURL(file);
                $("#uploadedImage").html(img);
                $("#uploadedImage").append('<br>');
            }
        })
    })
})