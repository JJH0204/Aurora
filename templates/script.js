// 포스트 데이터 예시
const posts = [
    {
        id: 1,
        imageUrl: 'sample/sample-post-image.jpg',
        content: '첫 번째 샘플 포스트입니다. 여기에 내용이 들어갑니다',
        userImage: 'sample/sample-user-image.png',
        nickname: 'User1',
        date: '2024-03-20',
        isLiked: false
    },
    
    {
        id: 2,
        imageUrl: 'sample/sample-post-image.jpg',
        content: '두 번째 샘플 포스트입니다. 여기에 내용이 들어갑니다',
        userImage: 'sample/sample-user-image.png',
        nickname: 'User2',
        date: '2024-03-20',
        isLiked: false
    },

    {
        id: 3,
        imageUrl: 'sample/sample-post-image.jpg',
        content: '세 번째 샘플 포스트입니다. 여기에 내용이 들어갑니다',
        userImage: 'sample/sample-user-image.png',
        nickname: 'User3',
        date: '2024-03-20',
        isLiked: false
    }
];

// 포스트 카드 생성 함수
function createPostCard(post) {
    const postCard = document.createElement('div');
    postCard.className = 'post-card';
    
    postCard.innerHTML = `
        <div class="post-image">
            <img src="${post.imageUrl}" alt="Post Image">
        </div>
        <div class="post-content">
            ${post.content}
        </div>
        <div class="post-footer">
            <div class="user-info">
                <img src="${post.userImage}" alt="User" class="user-image">
                <span class="nickname">${post.nickname}</span>
                <img src="img/like_${post.isLiked ? 'on' : 'off'}.png" 
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
        this.src = `img/like_${post.isLiked ? 'on' : 'off'}.png`;
        
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
    posts.forEach(post => {
        feed.appendChild(createPostCard(post));
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