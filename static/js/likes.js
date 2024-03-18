function likePost(postId) {
    let url = "/likes/post?post=" + postId;

    fetch(url, {
        method: "GET"
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // 在前端更新点赞数量
        document.getElementById('like-count').textContent = data.likes;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}


