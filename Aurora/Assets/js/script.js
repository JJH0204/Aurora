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
    // 디버깅을 위한 로그 추가
    console.log("Creating post card for:", post);

    if (!post) {
        console.error("Post data is undefined");
        return document.createElement('div'); // 빈 div 반환
    }

    const postCard = document.createElement('div');
    postCard.className = 'post-card';
    postCard.dataset.userId = post.user_id || '';
    postCard.dataset.isOfficial = post.is_official || false;

    // 헤더 영역 생성 (사용자 정보 + 좋아요)
    const headerDiv = document.createElement('div');
    headerDiv.className = 'post-header';

    // 사용자 정보 영역
    const userInfoContainer = document.createElement('div');
    userInfoContainer.className = 'user-info-container';

    // 프로필 이미지 로딩 수정
    const userImage = document.createElement('img');
    userImage.src = post.profile_image || '/static/img/default_profile.png';
    userImage.alt = 'User';
    userImage.className = 'user-image';
    userImage.onerror = () => {
        userImage.src = '/static/img/default_profile.png';
    };

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

    // 공식 계정 마크 추가 (is_official이 1인 경우)
    // tinyint를 고려하여 모든 가능한 true 케이스 처리
    if (post.is_official === 1 || post.is_official === true || post.is_official === '1') {
        console.log("Adding official mark for:", post.username);  // 디버깅용
        const officialMark = document.createElement('img');
        officialMark.src = '/static/img/official_mark.png';
        officialMark.alt = 'Official Account';
        officialMark.className = 'official-mark';
        officialMark.style.width = '16px';
        officialMark.style.height = '16px';
        officialMark.style.marginLeft = '4px';
        usernameContainer.appendChild(officialMark);
    }

    // DOM 구조 순서대로 조립
    userTextInfo.appendChild(usernameContainer);
    userInfoContainer.appendChild(userImage);
    userInfoContainer.appendChild(userTextInfo);
    headerDiv.appendChild(userInfoContainer);

    // 좋아요 버튼 영역
    const likeContainer = document.createElement('div');
    likeContainer.className = 'like-container';
    
    const likeButton = document.createElement('img');
    likeButton.className = 'like-icon';
    likeButton.src = post.is_liked ? '/static/img/like_on.png' : '/static/img/like_off.png';
    likeButton.alt = 'Like';
    
    const likeCount = document.createElement('span');
    likeCount.className = 'like-count';
    likeCount.textContent = post.like_count || 0;
    
    likeButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/like-post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    feed_id: post.feed_id
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'liked' || data.status === 'unliked') {
                // 현재 상태에 따라 다른 애니메이션 적용
                const animationClass = data.status === 'liked' ? 'animate-like' : 'animate-unlike';
                likeButton.classList.add(animationClass);
                
                // 이미지 변경
                likeButton.src = data.status === 'liked' 
                    ? '/static/img/like_on.png' 
                    : '/static/img/like_off.png';
                
                // 좋아요 수 업데이트
                likeCount.textContent = parseInt(likeCount.textContent) + (data.status === 'liked' ? 1 : -1);
                
                // 애니메이션 종료 후 클래스 제거
                setTimeout(() => {
                    likeButton.classList.remove(animationClass);
                }, data.status === 'liked' ? 600 : 400);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
    
    likeContainer.appendChild(likeButton);
    likeContainer.appendChild(likeCount);
    headerDiv.appendChild(likeContainer);
    
    postCard.appendChild(headerDiv);

    // aurora_db의 Feed-desc 테이블에서 desc 를 가져와서 출력
    const descriptionDiv = document.createElement('div');
    descriptionDiv.className = 'post-description';    // aurora_db의 Feed-desc 테이블에서 desc 를 가져와서 출력
    postCard.appendChild(descriptionDiv);

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
            video.src = getImageUrl(media.file_name);
            video.controls = true;
            mediaWrapper.appendChild(video);
        } else {
            const img = document.createElement('img');
            img.className = 'post-image';
            img.src = getImageUrl(media.file_name);
            img.alt = 'Post image';
            img.onerror = () => {
                console.log('Image load failed:', img.src);
            };
            img.onload = () => {
                console.log('Image loaded successfully:', img.src);
            };
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
                    video.play().catch(() => { });
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

    postCard.appendChild(mediaSlider);

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

        postCard.appendChild(contentDiv);
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
    postCard.appendChild(footerDiv);

    return postCard;
}
// 날짜 포맷팅 함수 추가
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}


document.addEventListener('DOMContentLoaded', function () {
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
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data); // 디버깅용 로그
            
            if (!data || !data.posts || !Array.isArray(data.posts)) {
                throw new Error('Invalid data format received from server');
            }

            if (data.posts.length === 0) {
                feed.innerHTML = '<p>표시할 게시물이 없습니다.</p>';
                return;
            }

            data.posts.forEach(post => {
                const postCard = createPostCard(post);
                feed.appendChild(postCard);
            });
        })
        .catch(error => {
            console.error('피드 게시물을 불러오는 중 오류 발생:', error);
            feed.innerHTML = `<p class="error-message">게시물을 불러올 수 없습니다: ${error.message}</p>`;
        });

    // Arrow 버튼 클릭 이벤트 추가
    const arrowButton = document.querySelector('.arrow-down');
    let currentPostIndex = 0;

    arrowButton.addEventListener('click', function () {
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
    mainContent.addEventListener('scroll', function () {
        const postCards = document.querySelectorAll('.post-card');
        const scrollPosition = mainContent.scrollTop;

        postCards.forEach((card, index) => {
            if (Math.abs(card.offsetTop - scrollPosition) < 50) {
                currentPostIndex = index;
            }
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const saveButton = document.querySelector('#saveChanges');
    if (saveButton) {
        saveButton.addEventListener('click', function (e) {
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
    element.addEventListener('click', function (e) {
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
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search');
    const searchResults = document.getElementById('searchResults');
    const search_img_btn = document.getElementById('search_img_btn');

    // 검색 기능 구현
    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {  // 엔터키가 눌렸을 때

            search_img_btn.click();

        }
    });
    search_img_btn.addEventListener('click', function () {

        const query = searchInput.value;

        if (query) {
            fetch(`/api/search_posts?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // 기존 피드 숨기기
                    const feed = document.querySelector('.feed');
                    feed.style.display = 'none';

                    // 검색 결과 표시
                    searchResults.innerHTML = '';

                    // 검색 결과가 없는 경우
                    if (!data.results || data.results.length === 0) {
                        const noResultsMsg = document.createElement('div');
                        noResultsMsg.className = 'no-results-message';
                        // noResultsMsg.textContent = '일치하는 관련 게시물이 없습니다.';
                        noResultsMsg.textContent = data.message;
                        searchResults.appendChild(noResultsMsg);
                        return;
                    }
                    // 검색 결과가 있는 경우 - createPostCard 함수를 사용하여 게시물 형태로 표시
                    data.results.forEach(post => {
                        const postCard = createPostCard({
                            id: post.id,
                            username: post.username,
                            desc: post.description,
                            media_files: post.media_files || [],
                            date: post.date,
                            like_count: post.like_count || 0,
                            isLiked: post.isLiked || false,
                            user_id: post.user_id,
                        });
                        searchResults.appendChild(postCard);
                    });
                })
                .catch(error => {
                    console.error('검색 중 오류 발생:', error);
                    // searchResults.innerHTML = '<div class="error-message">검색 중 오류가 발생했습니다.</div>';
                    searchResults.innerHTML = '<div class="error-message">검색 중 오류가 발생했습니다.</div>';
                });
        } else {
            // 검색어가 없는 경우 기존 피드 표시
            const feed = document.querySelector('.feed');
            feed.style.display = 'block';
            searchResults.innerHTML = '';
        }

    })
});

document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('searchButton');
    const searchResults = document.getElementById('searchResults');

    if (searchButton) {
        searchButton.addEventListener('click', function () {
            const searchInput = document.querySelector('.search');
            if (searchInput) {
                const query = searchInput.value.trim();
                if (query) {
                    fetch(`/api/search_posts?query=${encodeURIComponent(query)}`)
                        .then(response => response.json())
                        .then(data => {
                            // 검색 결과 표시
                            if (searchResults) {
                                searchResults.innerHTML = ''; // 이전 결과 초기화
                                if (data.results) {
                                    data.results.forEach(post => {
                                        const postElement = document.createElement('div');
                                        postElement.textContent = `${post.username}: ${post.description}`;
                                        searchResults.appendChild(postElement);
                                    });
                                }
                            }
                        })
                        .catch(error => {
                            console.error('검색 중 오류 발생:', error);
                        });
                }
            }
        });
    }
});

function updateImagePreview() {
    const input = document.getElementById('imageInput');
    const preview = document.querySelector('.image-preview');
    const initialUpload = document.querySelector('.initial-upload');
    const placeholder = preview.querySelector('.placeholder');
    if (input.files && input.files[0]) {
        // 초기 업로드 버튼 숨기기
        initialUpload.style.display = 'none';
        // 이미지 프리뷰 영역 보이기
        preview.style.display = 'flex';
        const reader = new FileReader();
        reader.onload = function (e) {
            placeholder.style.display = 'none';
            // 새로운 이미지 추가
            const img = document.createElement('img');
            img.src = e.target.result;
            preview.appendChild(img);
        }
        reader.readAsDataURL(input.files[0]);
    }
}