// 이미지 URL 생성 함수
function getImageUrl(imagePath, isStatic = false) {
    if (!imagePath) return '/static/img/default_post.png';
    
    // URL이 이미 완전한 경로인 경우 그대로 반환
    if (imagePath.startsWith('/media/') || imagePath.startsWith('/static/')) {
        return imagePath;
    }
    
    // 정적 이미지인 경우 static 경로 사용  
    if (isStatic) {
        return `/static/img/${imagePath}`;
    }
    // 동적 이미지인 경우 media 경로 사용
    return `/media/${imagePath}`;
}

// 시간 경과 계산 함수 추가
function getTimeAgo(dateString) {
    const now = new Date('2024-12-13T01:01:35+09:00');
    const date = new Date(dateString);
    const seconds = Math.floor((now - date) / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const months = Math.floor(days / 30);
    const years = Math.floor(days / 365);

    if (seconds < 60) return `${seconds}초 전`;
    if (minutes < 60) return `${minutes}분 전`;
    if (hours < 24) return `${hours}시간 전`;
    if (days < 30) return `${days}일 전`;
    if (months < 12) return `${months}달 전`;
    return `${years}년 전`;
}

// 포스트 카드 생성 함수
function createPostCard(post) {
    const card = document.createElement('div');
    card.className = 'post-card';
    card.dataset.userId = post.user_id;
    
    // 헤더 영역 생성 (사용자 정보 + 좋아요)
    const headerDiv = document.createElement('div');
    headerDiv.className = 'post-header';
    
    // 사용자 정보 영역
    const userInfoContainer = document.createElement('div');
    userInfoContainer.className = 'user-info-container';
    
    // 프로필 이미지 로딩
    const userImage = document.createElement('img');
    userImage.src = post.profile_image || '/static/img/default_profile.png';
    userImage.alt = 'User';
    userImage.className = 'user-image';
    
    const userTextInfo = document.createElement('div');
    userTextInfo.className = 'user-text-info';
    
    // 사용자 이름과 공식 계정 마크를 포함할 컨테이너
    const usernameContainer = document.createElement('div');
    usernameContainer.className = 'username-container';
    
    // 사용자 이름 표시
    const usernameSpan = document.createElement('span');
    usernameSpan.className = 'username';
    usernameSpan.textContent = `@${post.username}`;
    usernameContainer.appendChild(usernameSpan);
    
    // 공식 계정 마크 추가
    if (post.is_official === 1 || post.is_official === true || post.is_official === '1') {
        const officialMark = document.createElement('img');
        officialMark.src = '/static/img/official_mark.png';
        officialMark.alt = 'Official Account';
        officialMark.className = 'official-mark';
        usernameContainer.appendChild(officialMark);
    }
    
    userTextInfo.appendChild(usernameContainer);
    userInfoContainer.appendChild(userImage);
    userInfoContainer.appendChild(userTextInfo);
    
    // 좋아요 버튼 영역
    const likeContainer = document.createElement('div');
    likeContainer.className = 'like-container';
    
    const likeIcon = document.createElement('img');
    likeIcon.src = getImageUrl(`like_${post.isLiked ? 'on' : 'off'}.png`, true);
    likeIcon.alt = 'Like';
    likeIcon.className = 'like-icon';
    likeIcon.dataset.postId = post.id;
    
    const likeCount = document.createElement('span');
    likeCount.className = 'like-count';
    likeCount.textContent = post.likes || 0;
    
    likeContainer.appendChild(likeIcon);
    likeContainer.appendChild(likeCount);

    headerDiv.appendChild(userInfoContainer);
    headerDiv.appendChild(likeContainer);
    
    card.appendChild(headerDiv);

    // 미디어 파일 추가
    if (post.media_files && post.media_files.length > 0) {
        const mediaSlider = document.createElement('div');
        mediaSlider.className = 'media-slider';
        
        const mediaContainer = document.createElement('div');
        mediaContainer.className = 'media-container';
        
        post.media_files.forEach((media, index) => {
            const mediaWrapper = document.createElement('div');
            mediaWrapper.className = 'media-wrapper';
            
            if (media.extension_type === 'mp4' || media.extension_type === 'mov') {
                const video = document.createElement('video');
                video.className = 'post-video';
                video.src = getImageUrl(media.file_name);
                video.controls = true;
                mediaWrapper.appendChild(video);
            } else {
                const img = document.createElement('img');
                img.className = 'post-image';
                img.src = getImageUrl(media.file_name);
                img.alt = 'Post image';
                mediaWrapper.appendChild(img);
            }
            
            mediaContainer.appendChild(mediaWrapper);
        });
        
        mediaSlider.appendChild(mediaContainer);
        card.appendChild(mediaSlider);
    }

    // 설명 추가
    if (post.description) {
        const descriptionDiv = document.createElement('div');
        descriptionDiv.className = 'post-description';
        descriptionDiv.textContent = post.description;
        card.appendChild(descriptionDiv);
    }

    return card;
}

// 날짜 포맷팅 함수 추가
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// CSRF 토큰을 가져오는 부분
const csrftoken = document.querySelector('meta[name="csrf-token"]')?.content;

// toggleLike 함수 정의
function toggleLike(feedId) {
    if (!csrftoken) {
        console.error('CSRF token is missing');
        return;
    }

    fetch('/api/like-post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ feed_id: feedId })
    })
    .then(likedPostIds => {
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
                    media_files: post.media_files || [],
                    content: post.content,
                    userImage: post.userImage || 'default_profile.png',
                    username: post.username,
                    user_id: post.user_id,
                    date: post.date ? formatDate(post.date) : '날짜 없음',
                    like_count: post.like_count || 0,
                    isLiked: likedPostIds.includes(post.id),
                }));

                posts.forEach(post => {
                    const postCard = createPostCard(post);
                    feed.appendChild(postCard);
                });
            });
    })
    .catch(error => {
        console.error('피드 게시물을 불러오는 중 오류 발생:', error);
        const feed = document.querySelector('.feed');
        feed.innerHTML = '<p class="error-message">게시물을 불러올 수 없습니다. 잠시 후 다시 시도해주세요.</p>';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // CSRF 토큰을 가져오는 부분을 DOMContentLoaded 안으로 이동
    const csrftoken = document.querySelector('meta[name="csrf-token"]')?.content;

    function toggleLike(feedId) {
        if (!csrftoken) {
            console.error('CSRF token is missing'); // CSRF 토큰이 없을 경우 에러 로그
            return; // 함수 종료
        }

        fetch('/api/like-post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ feed_id: feedId })
        })
            .then(likedPostIds => {
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
                            media_files: post.media_files || [],
                            content: post.content,
                            userImage: post.userImage || 'default_profile.png',
                            username: post.username,
                            user_id: post.user_id,
                            date: post.date ? formatDate(post.date) : '날짜 없음',
                            like_count: post.like_count || 0,
                            isLiked: likedPostIds.includes(post.id),
                        }));

                        posts.forEach(post => {
                            const postCard = createPostCard(post);
                            feed.appendChild(postCard);
                        });
                    });
            })
            .catch(error => {
                console.error('피드 게시물을 불러오는 중 오류 발생:', error);
                const feed = document.querySelector('.feed');
                feed.innerHTML = '<p class="error-message">게시물을 불러올 수 없습니다. 잠시 후 다시 시도해주세요.</p>';
            });
    };

    const feed = document.querySelector('.feed');
    // 서버에서 피드 게시물 가져오기
    fetch('/api/feed-posts')
        .then(response => response.json())
        .then(data => {
            console.log('Received posts:', data.posts);  // 받은 데이터 확인
            
            data.posts.forEach(post => {
                const postCard = createPostCard(post);
                console.log('Created post card:', postCard);  // 생성된 카드 확인
                feed.appendChild(postCard);
                console.log('Post card added to feed');  // DOM 추가 확인
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

// 프로필 이미지 클릭 이벤트 핸들러 수정
document.querySelectorAll('.profile-image, .username').forEach(element => {
    element.style.cursor = 'pointer';  // 마우스 커서를 포인터로 변경
    element.addEventListener('click', function(e) {
        e.stopPropagation();  // 이벤트 버블링 방지
        
        // 사용자 정보가 있는 가장 가까운 부모 요소 찾기
        const postElement = this.closest('.post-card');
        if (postElement) {
            const user_id = postElement.dataset.user_id;  // 사용자 ID를 데이터 속성에서 가져옴
            // 프로필 페이지로 이동 (userId 기반)
            window.location.href = `/profile/${user_id}/`;
        }
    });
});

