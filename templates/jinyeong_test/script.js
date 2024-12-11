// 샘플 포스트 데이터
const samplePosts = [
    {
        postImage: 'sample/sample-post-image.jpg',
        content: '첫 번째 샘플 포스트입니다. 여기에 내용이 들어갑니다.',
        userImage: 'sample/sample-user-image.jpg',
        nickname: 'User1',
        date: '2024-03-20'
    },
    {
        postImage: 'sample/sample-post-image2.png',
        content: '두 번째 샘플 포스트입니다. 다양한 내용을 포함할 수 있습니다.',
        userImage: 'sample/sample-user-image.jpg',
        nickname: 'User2',
        date: '2024-03-21'
    },
    {
        postImage: 'sample/sample-post-image.jpg',
        content: '세 번째 샘플 포스트입니다. 이미지와 텍스트를 자유롭게 배치할 수 있습니다.',
        userImage: 'sample/sample-user-image.jpg',
        nickname: 'User3',
        date: '2024-03-22'
    }
];

// 포스트 생성 함수
function createPost(postData) {
    return `
        <div class="post-card">
            <div class="post-image">
                <img src="${postData.postImage}" alt="Post Image">
            </div>
            <div class="post-content">
                <p>${postData.content}</p>
            </div>
            <div class="post-footer">
                <div class="user-info">
                    <img src="${postData.userImage}" alt="User Profile" class="user-image">
                    <span class="nickname">${postData.nickname}</span>
                </div>
                <span class="date">${postData.date}</span>
            </div>
        </div>
    `;
}

// 피드 초기화 함수
function initializeFeed() {
    const feed = document.querySelector('.feed');
    if (!feed) return;

    feed.innerHTML = ''; // 기존 내용 초기화
    samplePosts.forEach(post => {
        feed.innerHTML += createPost(post);
    });
}

let currentPostIndex = 0;

// 화살표 클릭 시 다음 포스트로 이동
function scrollToNextPost() {
    const mainContent = document.querySelector('.main-content');
    const posts = document.querySelectorAll('.post-card');
    if (!posts.length) return;

    currentPostIndex = (currentPostIndex + 1) % posts.length;
    const targetPost = posts[currentPostIndex];
    
    mainContent.scrollTo({
        top: targetPost.offsetTop,
        behavior: 'smooth'
    });
}

// 이벤트 리스너 설정
document.addEventListener('DOMContentLoaded', () => {
    initializeFeed();
    
    // 로고 클릭 시 새로고침
    const logoButton = document.querySelector('.side-menu button:nth-child(3)');
    logoButton.addEventListener('click', () => {
        window.location.reload();
    });

    // 화살표 클릭 이벤트 추가
    const arrowDown = document.querySelector('.arrow-down');
    if (arrowDown) {
        arrowDown.addEventListener('click', scrollToNextPost);
    }
});
