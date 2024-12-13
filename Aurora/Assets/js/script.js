// 이미지 URL 생성 함수
function getImageUrl(imagePath, isStatic = false) {
    if (!imagePath) return '/static/img/default_post.png';
    
    // 정적 이미지인 경우 static 경로 사용  
    if (isStatic) {
        return `/static/img/${imagePath}`;
    }
    // 동적 이미지인 경우 media 경로 사용
    return `/${imagePath}`;
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

    // 헤더 영역 생성 (사용자 정보 + 좋아요)
    const headerDiv = document.createElement('div');
    headerDiv.className = 'post-header';
    
    // 사용자 정보 영역
    const userInfoContainer = document.createElement('div');
    userInfoContainer.className = 'user-info-container';
    
    const userImage = document.createElement('img');
    userImage.src = getImageUrl(post.userImage, true);
    userImage.alt = 'User';
    userImage.className = 'user-image';
    
    const userTextInfo = document.createElement('div');
    userTextInfo.className = 'user-text-info';
    
    // 사용자 이름 표시
    const usernameSpan = document.createElement('span');
    usernameSpan.className = 'username';
    usernameSpan.textContent = `@${post.username}`;
    
    userTextInfo.appendChild(usernameSpan);
    
    userInfoContainer.appendChild(userImage);
    userInfoContainer.appendChild(userTextInfo);
    userInfoContainer.onclick = () => window.location.href = `/profile/${post.user_id}/`;

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

    // 미디어 슬라이더 생성
    const mediaSlider = document.createElement('div');
    mediaSlider.className = 'media-slider';
    
    const mediaContainer = document.createElement('div');
    mediaContainer.className = 'media-container';
    
    // 미디어 파일들 추가
    post.media_files.forEach((media, index) => {
        const mediaWrapper = document.createElement('div');
        mediaWrapper.className = 'media-wrapper';
        
        if (media.extension_type === 'mp4' || media.extension_type === 'mov') {
            const video = document.createElement('video');
            video.className = 'post-video';
            video.src = `/media/${media.file_name}`;
            video.controls = true;
            mediaWrapper.appendChild(video);
        } else {
            const img = document.createElement('img');
            img.className = 'post-image';
            img.src = `/media/${media.file_name}`;
            img.alt = 'Post image';
            mediaWrapper.appendChild(img);
        }
        
        mediaContainer.appendChild(mediaWrapper);
    });
    
    mediaSlider.appendChild(mediaContainer);

    // 여러 미디어 파일이 있는 경우에만 네비게이션 추가
    if (post.media_files.length > 1) {
        const prevBtn = document.createElement('button');
        prevBtn.className = 'nav-btn prev-btn';
        prevBtn.innerHTML = '&#10094;';
        mediaSlider.appendChild(prevBtn);
        
        const nextBtn = document.createElement('button');
        nextBtn.className = 'nav-btn next-btn';
        nextBtn.innerHTML = '&#10095;';
        mediaSlider.appendChild(nextBtn);
        
        const pageIndicator = document.createElement('div');
        pageIndicator.className = 'page-indicator';
        post.media_files.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.className = `dot ${index === 0 ? 'active' : ''}`;
            pageIndicator.appendChild(dot);
        });
        mediaSlider.appendChild(pageIndicator);
        
        // 슬라이드 상태 및 기능
        let currentSlide = 0;
        const totalSlides = post.media_files.length;
        
        const updateSlide = (newIndex) => {
            currentSlide = newIndex;
            mediaContainer.style.transform = `translateX(-${currentSlide * 100}%)`;
            
            const dots = pageIndicator.querySelectorAll('.dot');
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
            
            const videos = mediaContainer.querySelectorAll('video');
            videos.forEach((video, index) => {
                if (index === currentSlide) {
                    video.play().catch(() => {});
                } else {
                    video.pause();
                    video.currentTime = 0;
                }
            });
        };
        
        prevBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const newIndex = (currentSlide - 1 + totalSlides) % totalSlides;
            updateSlide(newIndex);
        });
        
        nextBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const newIndex = (currentSlide + 1) % totalSlides;
            updateSlide(newIndex);
        });
        
        pageIndicator.addEventListener('click', (e) => {
            if (e.target.classList.contains('dot')) {
                const dots = Array.from(pageIndicator.children);
                const newIndex = dots.indexOf(e.target);
                updateSlide(newIndex);
            }
        });
    }
    
    card.appendChild(mediaSlider);

    // 게시글 내용 영역
    if (post.desc || post.content) {
        const contentDiv = document.createElement('div');
        contentDiv.className = 'post-content';
        
        // description(desc)이 있으면 먼저 표시
        if (post.desc) {
            const descriptionP = document.createElement('p');
            descriptionP.className = 'post-description';
            descriptionP.textContent = post.desc;
            contentDiv.appendChild(descriptionP);
        }
        
        // content가 있으면 그 다음에 표시
        if (post.content) {
            const contentP = document.createElement('p');
            contentP.className = 'post-text';
            contentP.textContent = post.content;
            contentDiv.appendChild(contentP);
        }
        
        card.appendChild(contentDiv);
    }

    // 푸터 영역 (날짜/시간)
    const footerDiv = document.createElement('div');
    footerDiv.className = 'post-footer';
    
    const dateDiv = document.createElement('div');
    dateDiv.className = 'date';
    const timeAgo = getTimeAgo(post.date);
    const fullDate = new Date(post.date).toLocaleString('ko-KR');
    dateDiv.textContent = `${timeAgo} (${fullDate})`;
    
    footerDiv.appendChild(dateDiv);
    card.appendChild(footerDiv);

    // 좋아요 기능
    likeIcon.addEventListener('click', function(e) {
        e.stopPropagation();
        const postId = this.dataset.postId;
        
        fetch('/check-auth/')
            .then(response => response.json())
            .then(data => {
                if (!data.isAuthenticated) {
                    alert('좋아요를 누르려면 로그인이 필요합니다.');
                    return;
                }
                fetch('/api/toggle-like', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        
                    },
                    body: JSON.stringify({ feed_id: postId })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                
                .then(data => {
                    if (data.is_liked !== undefined) {
                        this.src = getImageUrl(`like_${data.is_liked ? 'on' : 'off'}.png`, true);
                        likeCount.textContent = data.likes_count || 0;
                        
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
                    alert('좋아요 처리 중 오류가 발생했습니다.');
                });
            })
            .catch(error => {
                console.error('인증 확인 중 오류 발생:', error);
            });
    });

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



document.addEventListener('DOMContentLoaded', function() {
    const feed = document.querySelector('.feed');
    
    // 먼저 인증 상태 확인
    fetch('/check-auth/')
        .then(response => response.json())
        .then(authData => {
            // 로그인한 경우에만 좋아요 목록 가져오기
            if (authData.isAuthenticated) {
                return fetch('/api/check-liked-posts')
                    .then(response => response.json())
                    .then(likedData => likedData.liked_posts);
            }
            return [];  // 로그인하지 않은 경우 빈 배열 반환
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
                        nickname: post.nickname,
                        userId: post.userId,
                        date: post.date ? formatDate(post.date) : '날짜 없음',
                        likes: post.likes || 0,
                        isLiked: likedPostIds.includes(post.id),
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
            feed.innerHTML = '<p class="error-message">게시물을 불러올 수 없습니다. 잠시 후 다시 시도해주세요.</p>';
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
                media_files: post.media_files || [],
                content: post.content,
                userImage: post.userImage || 'default_profile.png',
                username: post.username,
                date: post.date,
                likes: post.likes || 0,
                isLiked: false,
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

// 게시물 목록을 렌더링하는 부분
data.posts.forEach(post => {
    const postElement = document.createElement('div');
    postElement.innerHTML = `
        <h3><a href="/profile/${post.user_id}/">${post.author}</a></h3>  <!-- 사용자 이름 클릭 시 프로필로 이동 -->
        <p>${post.description}</p>
        <img src="${post.image_url}" alt="Post Image">
        <p>Likes: ${post.likes}</p>
        <p>Comments: ${post.comments}</p>
    `;
    document.querySelector('.post-container').appendChild(postElement);
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
