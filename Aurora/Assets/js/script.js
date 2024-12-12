// 이미지 URL 생성 함수
function getImageUrl(imagePath, isStatic = false) {
    // 정적 이미지인 경우 static 경로 사용
    if (isStatic) {
        return `/static/img/${imagePath}`;
    }
    // 동적 이미지인 경우 media 경로 사용
    return `/media/${imagePath}`;
}

// 포스트 카드 생성 함수
function createPostCard(post) {
    const postCard = document.createElement('div');
    postCard.className = 'post-card';
    
    postCard.innerHTML = `
        <div class="post-image">
            <img src="${getImageUrl(post.imageUrl, post.isStaticImage)}" alt="Post Image">
        </div>
        <div class="post-content">
            ${post.content}
        </div>
        <div class="post-footer">
            <div class="post-user" onclick="window.location.href='/profile/${post.userId}/'">
                <img src="${getImageUrl(post.userImage, true)}" alt="User" class="user-image">
                <span class="nickname">${post.nickname}</span>
            </div>
            <div class="user-info">
                <img src="${getImageUrl(`like_${post.isLiked ? 'on' : 'off'}.png`, true)}" 
                     alt="Like" 
                     class="like-icon"
                     data-post-id="${post.id}"
                     style="width: 24px; height: 24px; margin-left: 10px; cursor: pointer;">
                <span class="like-count">${post.likes || 0}</span>
            </div>
            <div class="date">${post.date}</div>
        </div>
    `;

    // 좋아요 버튼 이벤트 리스너
    const likeIcon = postCard.querySelector('.like-icon');
    const likeCount = postCard.querySelector('.like-count');
    likeIcon.addEventListener('click', function() {
        const postId = this.dataset.postId;
        
        fetch('/api/toggle-like', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ feed_id: postId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_liked !== undefined) {
                // 좋아요 아이콘 변경
                this.src = getImageUrl(`like_${data.is_liked ? 'on' : 'off'}.png`, true);
                
                // 좋아요 카운트 업데이트
                const currentLikes = parseInt(likeCount.textContent);
                likeCount.textContent = data.is_liked ? currentLikes + 1 : currentLikes - 1;
                
                // 애니메이션 적용
                this.classList.remove('animate');
                void this.offsetWidth;
                this.classList.add('animate');
                
                setTimeout(() => {
                    this.classList.remove('animate');
                }, 500);
            }
        })
        .catch(error => {
            console.error('좋아요 토글 중 오류:', error);
        });
    });

    return postCard;
}

document.addEventListener('DOMContentLoaded', function() {
    const feed = document.querySelector('.feed');
    
    // 좋아요한 게시물 ID 목록 가져오기
    fetch('/api/check-liked-posts')
        .then(response => response.json())
        .then(likedData => {
            const likedPostIds = likedData.liked_posts;

            // 서버에서 피드 게시물 가져오기
            return fetch('/api/feed-posts')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // 서버에서 받은 데이터로 포스트 매핑
                    const posts = data.posts.map(post => ({
                        id: post.id,
                        imageUrl: post.imageUrl || 'default_post.png',
                        content: post.content,
                        userImage: post.userImage || 'people.png',
                        nickname: post.nickname,
                        date: post.date,
                        likes: post.likes || 0,
                        isLiked: likedPostIds.includes(post.id),
                        isStaticImage: post.imageUrl ? false : true
                    }));

                    // 기존 createPostCard 함수 사용하여 포스트 카드 생성
                    posts.forEach(post => {
                        const postCard = createPostCard(post);
                        feed.appendChild(postCard);
                    });
                });
        })
        .catch(error => {
            console.error('피드 게시물을 불러오는 중 오류 발생:', error);
            const feed = document.querySelector('.feed');
            feed.innerHTML = `<p>게시물을 불러올 수 없습니다: ${error.message}</p>`;
        });
});

// 페이지 로드 시 포스트 생성 및 arrow 버튼 이벤트 추가
document.addEventListener('DOMContentLoaded', function() {
    const feed = document.querySelector('.feed');
    // 서버에서 피드 게시물 가져오기
    fetch('/api/feed-posts')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // 서버에서 받은 데이터로 포스트 매핑
            const posts = data.posts.map(post => ({
                id: post.id,
                imageUrl: post.imageUrl || 'default_post.png',
                content: post.content,
                userImage: post.userImage || 'people.png',
                nickname: post.nickname,
                date: post.date,
                likes: post.likes || 0,
                isLiked: false,
                isStaticImage: post.imageUrl ? false : true
            }));

            // 기존 createPostCard 함수 사용하여 포스트 카드 생성
            posts.forEach(post => {
                const postCard = createPostCard(post);
                feed.appendChild(postCard);
            });
        })
        .catch(error => {
            console.error('피드 게시물을 불러오는 중 오류 발생:', error);
            const feed = document.querySelector('.feed');
            feed.innerHTML = `<p>게시물을 불러올 수 없습니다: ${error.message}</p>`;
        });

    // Arrow 버튼 클릭 이벤트 추가
    const arrowButton = document.querySelector('.arrow-down');
    let currentPostIndex = 0;

    arrowButton.addEventListener('click', function() {
        const mainContent = document.querySelector('.main-content');
        const postCards = document.querySelectorAll('.post-card');
        
        currentPostIndex = (currentPostIndex + 1) % postCards.length;
        const nextPost = postCards[currentPostIndex];
        
        // 부드러운 스크롤 효과
        mainContent.scrollTo({
            top: nextPost.offsetTop,
            behavior: 'smooth'
        });
    });

    // 스크롤 이벤트로 현재 포스트 인덱스 업데이트
    const mainContent = document.querySelector('.main-content');
    mainContent.addEventListener('scroll', function() {
        const postCards = document.querySelectorAll('.post-card');
        const scrollPosition = mainContent.scrollTop;
        
        postCards.forEach((card, index) => {
            if (Math.abs(card.offsetTop - scrollPosition) < 50) {
                currentPostIndex = index;
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.querySelector('#saveChanges');
    if (saveButton) {
        saveButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 입력값 가져오기
            const formData = {
                username: document.querySelector('#username').value.trim(),
                email: document.querySelector('#email').value.trim(),
                bio: document.querySelector('#bio').value.trim()
            };

            console.log('Sending data:', formData); // 디버깅용

            // CSRF 토큰 가져오기
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            fetch('/api/update-profile/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                    'Accept': 'application/json',
                    // CORS 헤더 추가
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                credentials: 'same-origin',  // 쿠키 포함
                body: JSON.stringify(formData)
            })
            .then(response => {
                console.log('Response status:', response.status); // 디버깅용
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data); // 디버깅용
                if (data.status === 'success') {
                    alert('프로필이 성공적으로 업데이트되었습니다.');
                    window.location.href = '/profile/';
                } else {
                    alert(data.message || '프로필 업데이트에 실패했습니다.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('프로필 업데이트 중 오류가 발생했습니다.');
            });
        });
    }
});
