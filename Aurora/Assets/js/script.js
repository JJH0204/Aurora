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
            </div>
            <div class="date">${post.date}</div>
        </div>
    `;

    // 좋아요 버튼 이벤트 리스너
    const likeIcon = postCard.querySelector('.like-icon');
    likeIcon.addEventListener('click', function() {
        const postId = this.dataset.postId;
        const post = posts.find(p => p.id == postId);
        post.isLiked = !post.isLiked;
        this.src = getImageUrl(`like_${post.isLiked ? 'on' : 'off'}.png`, true);
        
        // 애니메이션 적용
        this.classList.remove('animate'); // 기존 애니메이션 제거
        void this.offsetWidth; // 리플로우 강제 실행
        this.classList.add('animate'); // 새 애니메이션 추가
        
        // 애니메이션 종료 후 클래스 제거
        setTimeout(() => {
            this.classList.remove('animate');
        }, 500); // 애니메이션 지속 시간과 동일하게 설정
    });

    return postCard;
}

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

            // 입력값 검증
            if (!formData.username || !formData.email) {
                alert('사용자 이름과 이메일은 필수 입력 항목입니다.');
                return;
            }

            // 이메일 형식 검증
            if (!isValidEmail(formData.email)) {
                alert('올바른 이메일 형식을 입력해주세요.');
                return;
            }

            fetch('/api/update-profile/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('프로필이 성공적으로 업데이트되었습니다.');
                    // 프로필 페이지로 리다이렉트
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

    // 이메일 유효성 검사 함수
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Cancel 버튼 처리
    const cancelButton = document.querySelector('button.btn-secondary');
    if (cancelButton) {
        cancelButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/profile/';
        });
    }
});
