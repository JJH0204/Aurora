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
            return JsonResponse({'message': '이미 사용 중인 이메일입니다.'}, status=400)

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

        # 이메일로 사용자 찾기
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=401)

        # 비밀번호 확인 및 로그인
        user = authenticate(username=user.username, password=password)
        if user is not None:
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
                with open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb+') as destination:
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
def get_profile(request, user_id=None):
    try:
        # If user_id is provided, get that user's profile, otherwise get the current user's profile
        target_user = User.objects.get(id=user_id) if user_id else request.user
        
        profile_data = {
            'username': target_user.username,
            'email': target_user.email,
            'bio': target_user.profile.bio if hasattr(target_user, 'profile') else '',
            'profile_image': target_user.profile.profile_image.url if hasattr(target_user, 'profile') and target_user.profile.profile_image else None,
            'is_own_profile': request.user.id == target_user.id
        }
        return JsonResponse(profile_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_exempt
@login_required
def get_user_posts(request):
    try:
        user_id = request.user.id
        
        with connection.cursor() as cursor:
            # 사용자의 게시물 조회
            cursor.execute("""
                SELECT f.feed_id, fd.desc, 
                       (SELECT file_name FROM MEDIA_FILE WHERE feed_id = f.feed_id LIMIT 1) as image,
                       (SELECT COUNT(*) FROM COMMENT_INFO WHERE feed_id = f.feed_id) as comments_count,
                       f.like_count
                FROM FEED_INFO f
                LEFT JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
                WHERE f.user_id = %s
                ORDER BY f.feed_id DESC
            """, [user_id])
            
            posts = cursor.fetchall()
            
            return JsonResponse({
                'posts': [{
                    'id': post[0],
                    'description': post[1],
                    'image_url': f'/media/{post[2]}' if post[2] else None,
                    'comments': post[3],
                    'likes': post[4]
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
def update_profile(request):
    print("Method:", request.method)  # 요청 메소드 확인
    
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    try:
        # 요청 데이터 확인
        print("Request body:", request.body.decode('utf-8'))
        data = json.loads(request.body.decode('utf-8'))
        
        username = data.get('username')
        email = data.get('email')
        bio = data.get('bio', '')
        
        print(f"Received data - username: {username}, email: {email}, bio: {bio}")

        with connection.cursor() as cursor:
            try:
                # 현재 사용자 정보 확인
                cursor.execute("SELECT * FROM USER_INFO WHERE user_id = 1")
                user_info = cursor.fetchone()
                print("Current user info:", user_info)

                # USER_INFO 업데이트
                cursor.execute("""
                    UPDATE USER_INFO 
                    SET username = %s 
                    WHERE user_id = 1
                """, [username])
                print("USER_INFO updated")

                # USER_ACCESS 업데이트
                cursor.execute("""
                    UPDATE USER_ACCESS 
                    SET email = %s 
                    WHERE user_id = 1
                """, [email])
                print("USER_ACCESS updated")

                return JsonResponse({
                    'status': 'success',
                    'message': '프로필이 성공적으로 업데이트되었습니다.',
                    'data': {
                        'username': username,
                        'email': email,
                        'bio': bio
                    }
                })

            except Exception as db_error:
                print("Database error:", str(db_error))
                print("Traceback:", traceback.format_exc())
                return JsonResponse({
                    'status': 'error',
                    'message': f'데이터베이스 오류: {str(db_error)}'
                }, status=500)

    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))
        return JsonResponse({
            'status': 'error',
            'message': '잘못된 JSON 형식입니다.'
        }, status=400)
    
    except Exception as e:
        print("Unexpected error:", str(e))
        print("Traceback:", traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': f'서버 오류: {str(e)}'
        }, status=500)

@csrf_exempt
def get_feed_posts(request):
    try:
        with connection.cursor() as cursor:
            # 모든 게시물 쿼리
            cursor.execute("""
                SELECT 
                    f.feed_id, 
                    fd.`desc`, 
                    u.username, 
                    mf.file_name,
                    f.like_count,
                    f.feed_type
                FROM FEED_INFO f
                LEFT JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
                LEFT JOIN USER_INFO u ON f.user_id = u.user_id
                LEFT JOIN MEDIA_FILE mf ON f.feed_id = mf.feed_id
                GROUP BY f.feed_id
                ORDER BY f.feed_id DESC
            """)
            
            feeds = cursor.fetchall()

            posts = [{
                'id': feed[0],
                'content': feed[1] or '',
                'nickname': feed[2] or 'Unknown',
                'imageUrl': feed[3] or 'default_post.png',
                'likes': feed[4] or 0,
                'date': datetime.now().strftime('%Y-%m-%d')  # 현재 날짜 사용
            } for feed in feeds]

        return JsonResponse({'posts': posts})

    except Exception as e:
        print(f"Error fetching feed posts: {str(e)}")
        return JsonResponse({
            'message': f'피드 게시물을 불러오는 중 오류가 발생했습니다: {str(e)}',
            'error': str(e)
        }, status=500)