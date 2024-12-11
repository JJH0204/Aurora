from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import bcrypt
import os
from django.conf import settings

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

        with connection.cursor() as cursor:
            # 이메일 중복 검사
            cursor.execute("SELECT email FROM USER_ACCESS WHERE email = %s", [email])
            if cursor.fetchone():
                return JsonResponse({'message': '이미 사용 중인 이메일입니다.'}, status=400)

            # 새로운 user_id 생성
            cursor.execute("SELECT MAX(user_id) FROM USER_INFO")
            max_id = cursor.fetchone()[0]
            new_user_id = 1 if max_id is None else max_id + 1

            # 비밀번호 해싱
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # USER_INFO에 사용자 추가
            cursor.execute("""
                INSERT INTO USER_INFO (user_id, is_admin, is_official, username, bf_list)
                VALUES (%s, %s, %s, %s, %s)
            """, [new_user_id, False, False, username, ""])

            # USER_ACCESS에 인증 정보 추가
            cursor.execute("""
                INSERT INTO USER_ACCESS (user_id, email, password)
                VALUES (%s, %s, %s)
            """, [new_user_id, email, hashed_password.decode('utf-8')])

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

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ua.user_id, ua.password, ui.username 
                FROM USER_ACCESS ua 
                JOIN USER_INFO ui ON ua.user_id = ui.user_id 
                WHERE ua.email = %s
            """, [email])
            
            user = cursor.fetchone()
            if not user or not bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                return JsonResponse({'message': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=401)

            # 세션에 사용자 정보 저장
            request.session['user_id'] = user[0]
            request.session['username'] = user[2]

            return JsonResponse({'message': '로그인 성공'})

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return JsonResponse({'message': '로그인 처리 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
def create_post(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    if 'user_id' not in request.session:
        return JsonResponse({'message': '로그인이 필요합니다.'}, status=401)

    try:
        user_id = request.session['user_id']
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
def get_profile(request):
    if 'user_id' not in request.session:
        return JsonResponse({'message': '로그인이 필요합니다.'}, status=401)

    try:
        user_id = request.session['user_id']
        
        with connection.cursor() as cursor:
            # 사용자 정보 조회
            cursor.execute("""
                SELECT u.user_id, u.user_name, u.user_desc, u.profile_image,
                       (SELECT COUNT(*) FROM FEED_INFO WHERE user_id = u.user_id) as posts_count,
                       (SELECT COUNT(*) FROM USER_ACCESS WHERE followed_id = u.user_id) as followers_count,
                       (SELECT COUNT(*) FROM USER_ACCESS WHERE follower_id = u.user_id) as following_count
                FROM USER_INFO u
                WHERE u.user_id = %s
            """, [user_id])
            
            user = cursor.fetchone()
            
            if not user:
                return JsonResponse({'message': '사용자를 찾을 수 없습니다.'}, status=404)
            
            return JsonResponse({
                'username': user[1],
                'bio': user[2] or '',
                'profile_image': user[3] if user[3] else None,
                'posts_count': user[4],
                'followers_count': user[5],
                'following_count': user[6]
            })

    except Exception as e:
        print(f"Error fetching profile: {str(e)}")
        return JsonResponse({'message': '프로필 정보를 불러오는 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt
def get_user_posts(request):
    if 'user_id' not in request.session:
        return JsonResponse({'message': '로그인이 필요합니다.'}, status=401)

    try:
        user_id = request.session['user_id']
        
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
def get_user_friends(request):
    if 'user_id' not in request.session:
        return JsonResponse({'message': '로그인이 필요합니다.'}, status=401)

    try:
        user_id = request.session['user_id']
        
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
def get_liked_posts(request):
    if 'user_id' not in request.session:
        return JsonResponse({'message': '로그인이 필요합니다.'}, status=401)

    try:
        user_id = request.session['user_id']
        
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
