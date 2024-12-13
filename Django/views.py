from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
import json
import bcrypt
import os
from django.conf import settings
import traceback  # 상세한 오류 추적을 위해 추가
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.db import transaction


@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not all([email, username, password]):
            return JsonResponse({'message': '모든 필드를 입력해주세요.'}, status=400)

        # 이메일 중복 검사
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': '이메일 사용 중인 이메일입니다.'}, status=400)

        # Django User 모델을 사용하여 사용자 생성
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password  # Django가 자동으로 비밀번호를 해시화합니다
        )

        # USER_INFO 테이블에 추가 정보 저장
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USER_INFO (user_id, is_admin, is_official, username, bf_list)
                VALUES (%s, %s, %s, %s, %s)
            """, [user.id, False, False, username, ""])
            
        # USER_ACCESS 테이블에 추가 정보 저장
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO USER_ACCESS (user_id, email, password)
                VALUES (%s, %s, %s)
            """, [user.id, email, password])  # 수정된 부분

        return JsonResponse({'message': '회원가입이 완료되었습니다.'})

    except Exception as e:
        print(f"Error during signup: {str(e)}")
        return JsonResponse({'message': '회원가입 처리 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return JsonResponse({'message': '이메일과 비밀번호를 모두 입력해주세요.'}, status=400)

        # USER_ACCESS 테이블에서 사용자 확인
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ua.user_id, ua.password, u.username 
                FROM USER_ACCESS ua
                JOIN auth_user u ON ua.user_id = u.id
                WHERE ua.email = %s
            """, [email])
            result = cursor.fetchone()
            
            if result and result[1] == password:  # 비밀번호 일치
                user = User.objects.get(id=result[0])
                auth_login(request, user)
                return JsonResponse({'message': '로그인 성공'})
            else:
                return JsonResponse({'message': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=401)

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return JsonResponse({'message': '로그인 처리 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    auth_logout(request)
    return JsonResponse({'message': '로그아웃 성공'})

@csrf_exempt
@login_required
def create_post(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    try:
        user_id = request.user.id
        description = request.POST.get('description')
        
        if not description:
            return JsonResponse({'message': '게시물 내용을 입력해주세요.'}, status=400)

        with connection.cursor() as cursor:
            # 새로운 feed_id 생성
            cursor.execute("SELECT MAX(feed_id) FROM FEED_INFO")
            max_id = cursor.fetchone()[0]
            new_feed_id = 1 if max_id is None else max_id + 1

            # FEED_INFO에 게시물 추가
            cursor.execute("""
                INSERT INTO FEED_INFO (feed_id, user_id, like_count, feed_type)
                VALUES (%s, %s, %s, %s)
            """, [new_feed_id, user_id, 0, 'type1'])

            # FEED_DESC에 게시물 내용 추가
            cursor.execute("""
                INSERT INTO FEED_DESC (feed_id, `desc`)
                VALUES (%s, %s)
            """, [new_feed_id, description])

            # 이미지 파일 처리
            for i in range(10):  # 최대 10개의 이미지
                if f'image{i}' not in request.FILES:
                    continue

                image = request.FILES[f'image{i}']
                file_name = f'post_{new_feed_id}_{i}{os.path.splitext(image.name)[1]}'
                
                # 파일 저장
                save_path = os.path.join(settings.MEDIA_ROOT)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                    
                with open(os.path.join(save_path, file_name), 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # MEDIA_FILE에 파일 정보 추가
                cursor.execute("""
                    INSERT INTO MEDIA_FILE (media_id, file_name, extension_type, feed_id, media_number)
                    VALUES ((SELECT COALESCE(MAX(media_id), 0) + 1 FROM MEDIA_FILE m2), %s, %s, %s, %s)
                """, [file_name, os.path.splitext(image.name)[1][1:], new_feed_id, i])

        return JsonResponse({'message': '게시물이 성공적으로 업로드되었습니다.'})

    except Exception as e:
        print(f"Error during post creation: {str(e)}")
        return JsonResponse({'message': '게시물 업로드 중 오류가 발생했습니다.'}, status=500)


@csrf_exempt
@login_required
def get_user_posts(request):
    try:
        user_id = request.user.id
        
        with connection.cursor() as cursor:
            # 사용자의 게시물 조회
            cursor.execute("""
                SELECT f.feed_id, fd.desc, u.username, 
                       (SELECT file_name FROM MEDIA_FILE WHERE feed_id = f.feed_id LIMIT 1) as image,
                       (SELECT COUNT(*) FROM COMMENT_INFO WHERE feed_id = f.feed_id) as comments_count,
                       f.like_count
                FROM FEED_INFO f
                LEFT JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
                LEFT JOIN USER_INFO u ON f.user_id = u.user_id
                WHERE f.user_id = %s
                ORDER BY f.feed_id DESC
            """, [user_id])
            
            posts = cursor.fetchall()
            print(f"Fetched posts: {posts}")  # 쿼리 결과 출력
            
            return JsonResponse({
                'posts': [{
                    'id': post[0],
                    'description': post[1],
                    'author': post[2] if post[2] else 'Unknown',  # 사용자 이름이 없을 경우 처리
                    'image_url': f'/media/{post[3]}' if post[3] else None,
                    'comments': post[4],
                    'likes': post[5]
                } for post in posts]
            })

    except Exception as e:
        print(f"Error fetching posts: {str(e)}")
        return JsonResponse({'message': '게시물을 불러오는 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
@login_required
def get_user_friends(request):
    try:
        user_id = request.user.id
        
        with connection.cursor() as cursor:
            # 팔로잉 중인 사용자 목록 조회
            cursor.execute("""
                SELECT u.user_id, u.user_name, u.profile_image
                FROM USER_INFO u
                INNER JOIN USER_ACCESS ua ON u.user_id = ua.followed_id
                WHERE ua.follower_id = %s
                ORDER BY u.user_name
            """, [user_id])
            
            friends = cursor.fetchall()
            
            return JsonResponse({
                'friends': [{
                    'id': friend[0],
                    'username': friend[1],
                    'profile_image': f'/media/{friend[2]}' if friend[2] else None
                } for friend in friends]
            })

    except Exception as e:
        print(f"Error fetching friends: {str(e)}")
        return JsonResponse({'message': '친구 목록을 불러오는 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
@login_required
def get_liked_posts(request):
    try:
        user_id = request.user.id
        
        with connection.cursor() as cursor:
            # 사용자가 좋아요한 게시물 조회
            cursor.execute("""
                SELECT f.feed_id, fd.desc, u.user_name,
                       (SELECT file_name FROM MEDIA_FILE WHERE feed_id = f.feed_id LIMIT 1) as image,
                       (SELECT COUNT(*) FROM COMMENT_INFO WHERE feed_id = f.feed_id) as comments_count,
                       f.like_count
                FROM FEED_INFO f
                INNER JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
                INNER JOIN USER_INFO u ON f.user_id = u.user_id
                INNER JOIN FEED_LIKE fl ON f.feed_id = fl.feed_id
                WHERE fl.user_id = %s
                ORDER BY fl.like_date DESC
            """, [user_id])
            
            posts = cursor.fetchall()
            
            return JsonResponse({
                'posts': [{
                    'id': post[0],
                    'description': post[1],
                    'author': post[2],
                    'image_url': f'/media/{post[3]}' if post[3] else None,
                    'comments': post[4],
                    'likes': post[5]
                } for post in posts]
            })

    except Exception as e:
        print(f"Error fetching liked posts: {str(e)}")
        return JsonResponse({'message': '좋아요한 게시물을 불러오는 중 오류가 발생했습니다.'}, status=500)


@csrf_exempt
@login_required
def get_profile(request, user_id=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ui.username, ua.email, ui.profile_image, ui.bio
                FROM USER_INFO ui
                JOIN USER_ACCESS ua ON ui.user_id = ua.user_id
                WHERE ui.user_id = %s
            """, [user_id if user_id else request.user.id])
            
            user_data = cursor.fetchone()
            if not user_data:
                return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
            
            return JsonResponse({
                'username': user_data[0],
                'email': user_data[1],
                'profile_image': f'/media/{user_data[2]}' if user_data[2] else None,
                'bio': user_data[3] or ''  # bio 정보 추가
            })
    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return JsonResponse({'error': '프로필을 불러오는 중 오류가 발생했습니다.'}, status=500)


@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            # 프로필 이미지 처리
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                
                # 저장 경로 수정
                profile_images_dir = os.path.join(settings.MEDIA_ROOT, 'Profile_images')
                os.makedirs(profile_images_dir, exist_ok=True)
                
                # 파일명 설정
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_extension = os.path.splitext(profile_image.name)[1]
                new_filename = f"{request.user.username}_{timestamp}{file_extension}"
                
                # 상대 경로로 저장 (DB에 저장될 경로)
                relative_path = f"Profile_images/{new_filename}"
                
                # 전체 경로 (실제 파일 저장 위치)
                file_path = os.path.join(profile_images_dir, new_filename)
                
                # 파일 저장
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_image.chunks():
                        destination.write(chunk)
                
                # DB에 상대 경로 저장
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE USER_INFO 
                        SET profile_image = %s 
                        WHERE user_id = %s
                    """, [relative_path, request.user.id])

            # JSON 데이터에서 bio 가져오기 추가
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            bio = data.get('bio', '')  # bio 데이터 추가

            with connection.cursor() as cursor:
                # USER_INFO 테이블 업데이트 시 bio도 함께 업데이트
                cursor.execute("""
                    UPDATE USER_INFO 
                    SET username = %s,
                        bio = %s  # bio 컬럼 업데이트 추가
                    WHERE user_id = %s
                """, [username, bio, request.user.id])

                # USER_ACCESS 테이블 업데이트
                cursor.execute("""
                    UPDATE USER_ACCESS 
                    SET email = %s 
                    WHERE user_id = %s
                """, [email, request.user.id])

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)

@csrf_exempt
def get_feed_posts(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH RankedMedia AS (
                SELECT 
                    mf.feed_id,
                    mf.file_name,
                    mf.extension_type,
                    ROW_NUMBER() OVER (PARTITION BY mf.feed_id ORDER BY mf.media_number) as rn
                FROM MEDIA_FILE mf
            )
            SELECT 
                f.feed_id, 
                fd.`desc`, 
                ui.username,
                rm.file_name,
                f.like_count,
                f.feed_type,
                ui.user_id,
                rm.extension_type
            FROM FEED_INFO f
            LEFT JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
            LEFT JOIN USER_INFO ui ON f.user_id = ui.user_id
            LEFT JOIN RankedMedia rm ON f.feed_id = rm.feed_id AND rm.rn = 1
            ORDER BY f.feed_id DESC
        """)
        
        columns = [col[0] for col in cursor.description]
        feeds = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # 로그인한 사용자의 좋아요 상태 확인
        liked_posts = set()
        if request.user.is_authenticated:
            cursor.execute("""
                SELECT feed_id FROM FEED_LIKE WHERE user_id = %s
            """, [request.user.id])
            liked_posts = {row[0] for row in cursor.fetchall()}
        
        for feed in feeds:
            feed['isLiked'] = feed['feed_id'] in liked_posts
            
            # 각 게시물의 모든 미디어 파일 가져오기
            cursor.execute("""
                SELECT file_name, extension_type
                FROM MEDIA_FILE
                WHERE feed_id = %s
            """, [feed['feed_id']])
            media_files = cursor.fetchall()
            feed['media_files'] = [{'file_name': file[0], 'extension_type': file[1]} for file in media_files]
        
        return JsonResponse({'posts': feeds}, json_dumps_params={'ensure_ascii': False})

@login_required
@csrf_exempt
def toggle_like(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    try:
        # JSON 데이터 파싱
        data = json.loads(request.body)
        feed_id = data.get('feed_id')
        user_id = request.user.id

        # 유효성 검사
        if not feed_id:
            return JsonResponse({'message': 'feed_id가 필요합니다.'}, status=400)

        # feed_id가 FEED_INFO에 존재하는지 확인
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM FEED_INFO WHERE feed_id = %s", [feed_id])
            if cursor.fetchone()[0] == 0:
                return JsonResponse({'message': '존재하지 않는 게시물입니다.'}, status=404)

        with transaction.atomic():
            # 이미 좋아요를 눌렀는지 확인
            with connection.cursor() as cursor:
                print(f"Checking if user {user_id} already liked post {feed_id}")  # 로그 추가
                cursor.execute("""
                    SELECT COUNT(*) FROM FEED_LIKE 
                    WHERE user_id = %s AND feed_id = %s
                """, [user_id, feed_id])
                is_already_liked = cursor.fetchone()[0] > 0

            if is_already_liked:
                # 좋아요 취소
                with connection.cursor() as cursor:
                    print(f"User {user_id} is unliking post {feed_id}")  # 로그 추가
                    cursor.execute("""
                        DELETE FROM FEED_LIKE 
                        WHERE user_id = %s AND feed_id = %s
                    """, [user_id, feed_id])
                    
                    # FEED_INFO의 like_count 감소
                    cursor.execute("""
                        UPDATE FEED_INFO 
                        SET like_count = GREATEST(like_count - 1, 0)
                        WHERE feed_id = %s
                    """, [feed_id])
                
                return JsonResponse({
                    'message': '좋아요 취소됨', 
                    'is_liked': False,
                    'likes_count': get_likes_count(feed_id)
                })
            else:
                # 좋아요 추가
                with connection.cursor() as cursor:
                    print(f"User {user_id} is liking post {feed_id}")  # 로그 추가
                    cursor.execute("""
                        INSERT INTO FEED_LIKE (user_id, feed_id, like_date) 
                        VALUES (%s, %s, NOW())
                    """, [user_id, feed_id])
                    
                    # FEED_INFO의 like_count 증가
                    cursor.execute("""
                        UPDATE FEED_INFO 
                        SET like_count = like_count + 1 
                        WHERE feed_id = %s
                    """, [feed_id])
                
                return JsonResponse({
                    'message': '좋아요 완료', 
                    'is_liked': True,
                    'likes_count': get_likes_count(feed_id)
                })

    except json.JSONDecodeError:
        return JsonResponse({'message': '잘못된 JSON 형식입니다.'}, status=400)
    except Exception as e:
        print(f"Error during like toggle: {str(e)}")
        return JsonResponse({'message': '좋아요 처리 중 오류가 발생했습니다.'}, status=500)

def get_likes_count(feed_id):
    """특정 피드의 좋아요 수를 반환하는 헬퍼 함수"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT like_count FROM FEED_INFO 
            WHERE feed_id = %s
        """, [feed_id])
        result = cursor.fetchone()
        return result[0] if result else 0

@csrf_exempt
@login_required
def check_liked_posts(request):
    try:
        user_id = request.user.id
        
        with connection.cursor() as cursor:
            # 사용자가 좋아요한 게시물 ID 목록 조회
            cursor.execute("""
                SELECT feed_id FROM FEED_LIKE 
                WHERE user_id = %s
            """, [user_id])
            
            liked_feed_ids = [row[0] for row in cursor.fetchall()]
            
        return JsonResponse({
            'liked_posts': liked_feed_ids
        })

    except Exception as e:
        print(f"Error checking liked posts: {str(e)}")
        return JsonResponse({'message': '좋아요한 게시물 확인 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
def check_auth(request):
    return JsonResponse({
        'isAuthenticated': request.user.is_authenticated
    })

@csrf_exempt
@login_required
def like_post(request):
    try:
        data = json.loads(request.body)
        feed_id = data.get('feed_id')
        user_id = request.user.id

        with connection.cursor() as cursor:
            # 이미 좋아요를 눌렀는지 확인
            cursor.execute("""
                SELECT COUNT(*) 
                FROM LIKE_INFO 
                WHERE feed_id = %s AND user_id = %s
            """, [feed_id, user_id])
            
            already_liked = cursor.fetchone()[0] > 0

            if already_liked:
                # 좋아요 취소
                cursor.execute("""
                    DELETE FROM LIKE_INFO 
                    WHERE feed_id = %s AND user_id = %s
                """, [feed_id, user_id])

                # 좋아요 수 감소
                cursor.execute("""
                    UPDATE FEED_INFO 
                    SET like_count = like_count - 1 
                    WHERE feed_id = %s
                """, [feed_id])

                return JsonResponse({'status': 'unliked', 'message': '좋아요가 취소되었습니다.'})
            else:
                # 좋아요 추가
                cursor.execute("""
                    INSERT INTO LIKE_INFO (feed_id, user_id) 
                    VALUES (%s, %s)
                """, [feed_id, user_id])

                # 좋아요 수 증가
                cursor.execute("""
                    UPDATE FEED_INFO 
                    SET like_count = like_count + 1 
                    WHERE feed_id = %s
                """, [feed_id])

                return JsonResponse({'status': 'liked', 'message': '좋아요가 추가되었습니다.'})

    except Exception as e:
        print(f"Error in like_post: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)