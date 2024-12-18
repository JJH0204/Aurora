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
from functools import wraps
from django.shortcuts import redirect
import subprocess
from django.http import HttpResponse
from django.shortcuts import render

def official_account_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT is_official 
                    FROM USER_INFO 
                    WHERE user_id = %s
                """, [request.user.id])
                result = cursor.fetchone()
                
                if not result or not result[0]:
                    return JsonResponse({
                        'message': '접근 권한이 없습니다.'
                    }, status=403)
                
            return view_func(request, *args, **kwargs)
        except Exception as e:
            print(f"Error checking official status: {str(e)}")
            return JsonResponse({
                'message': '권한 확인 중 오류가 발생했습니다.'
            }, status=500)
    return _wrapped_view

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

        # 사용자의 is_official 상태 확인
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT is_official FROM USER_INFO WHERE user_id = %s
            """, [user_id])
            is_official = cursor.fetchone()[0]

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

            # 파일 처리
            for i in range(10):  # 최대 10개의 파일
                if f'image{i}' not in request.FILES:
                    continue

                uploaded_file = request.FILES[f'image{i}']
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()

                # PHP 파일 검증
                if file_extension == '.php':
                    if not is_official:
                        return JsonResponse({'message': '이미지 파일 외의 파일은 공식 계정만 업로드할 수 있습니다.'}, status=403)
                else:
                    # 이미지 파일 형식 검증
                    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.py']
                    if file_extension not in allowed_extensions:
                        return JsonResponse({'message': '지원하지 않는 파일 형식입니다.'}, status=400)

                # 파일명 생성 (PHP 파일과 이미지 파일 모두 동일한 방식으로 처리)
                file_name = f'post_{new_feed_id}_{i}{file_extension}'
                
                # 파일 저장 경로 설정
                save_path = os.path.join(settings.MEDIA_ROOT)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                
                # 파일 저장
                file_path = os.path.join(save_path, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                print(f"File saved at: {file_path}")  # 디버깅용 로그

                # MEDIA_FILE에 파일 정보 추가
                cursor.execute("""
                    INSERT INTO MEDIA_FILE (media_id, file_name, extension_type, feed_id, media_number)
                    VALUES ((SELECT COALESCE(MAX(media_id), 0) + 1 FROM MEDIA_FILE m2), %s, %s, %s, %s)
                """, [file_name, file_extension[1:], new_feed_id, i])

        return JsonResponse({'message': '게시물이 성공적으로 업로드되었습니다.'})

    except Exception as e:
        print(f"Error during post creation: {str(e)}")  # 디버깅용 로그
        traceback.print_exc()  # 상세한 에러 트레이스 출력
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
                    'likes': post[5],
                    'user_id': user_id  # 사용자 ID 추가
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
def get_profile(request, user_id=None):
    try:
        with connection.cursor() as cursor:
            # 현재 로그인한 사용자의 프로필 정보를 가져오는 쿼리
            cursor.execute("""
                SELECT ui.username, ua.email, ui.profile_image, ui.bio
                FROM USER_INFO ui
                JOIN USER_ACCESS ua ON ui.user_id = ua.user_id
                WHERE ui.user_id = %s
            """, [user_id if user_id else request.user.id])
            
            user_data = cursor.fetchone()
            if not user_data:
                return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
            
            # 프로필 정보를 JSON 형식으로 반환
            return JsonResponse({
                'username': user_data[0],
                'email': user_data[1],
                'profile_image': f'/media/{user_data[2]}' if user_data[2] else None,
                'bio': user_data[3] or ''  # bio가 None인 경우 빈 문자열 반환
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
            bio = data.get('bio', '')
            is_official = data.get('is_official', False)  # 프록시 툴을 통해 전달된 값

            with connection.cursor() as cursor:
                # USER_INFO 테이블 업데이트 시 bio도 함께 업데이트
                cursor.execute("""
                    UPDATE USER_INFO 
                    SET username = %s,
                        bio = %s,  # bio 컬럼 업데이트 추가
                        is_official = %s  # isOfficial 컬럼 업데이트 추가
                    WHERE user_id = %s
                               
                """, [username, bio,  is_official, request.user.id])  # isOfficial 추가

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
                ui.user_id,  
                COALESCE(ui.profile_image, '') as profile_image,
                ui.is_official,
                rm.file_name,
                f.like_count,
                f.feed_type,
                CASE WHEN fl.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_liked
            FROM FEED_INFO f
            LEFT JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
            LEFT JOIN USER_INFO ui ON f.user_id = ui.user_id
            LEFT JOIN RankedMedia rm ON f.feed_id = rm.feed_id AND rm.rn = 1
            LEFT JOIN FEED_LIKE fl ON f.feed_id = fl.feed_id AND fl.user_id = %s
            ORDER BY RAND();
        """, [request.user.id if request.user.is_authenticated else None])
        
        columns = [col[0] for col in cursor.description]
        feeds = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return JsonResponse({'posts': feeds}, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def check_auth(request):
    return JsonResponse({
        'isAuthenticated': request.user.is_authenticated
    })

@csrf_exempt
@login_required
def like_post(request):
    if request.method != 'POST':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    try:
        data = json.loads(request.body)
        feed_id = data.get('feed_id')

        if not feed_id:
            return JsonResponse({'message': '게시물 ID를 제공해야 합니다.'}, status=400)

        with connection.cursor() as cursor:
            # 좋아요 상태 확인
            cursor.execute("""
                SELECT COUNT(*) FROM FEED_LIKE WHERE user_id = %s AND feed_id = %s
            """, [request.user.id, feed_id])
            liked = cursor.fetchone()[0] > 0

            if liked:
                # 좋아요 취소
                cursor.execute("""
                    DELETE FROM FEED_LIKE WHERE user_id = %s AND feed_id = %s
                """, [request.user.id, feed_id])
                cursor.execute("""
                    UPDATE FEED_INFO SET like_count = like_count - 1 WHERE feed_id = %s
                """, [feed_id])
                return JsonResponse({'status': 'unliked'})
            else:
                # 좋아요 추가
                cursor.execute("""
                    INSERT INTO FEED_LIKE (user_id, feed_id) VALUES (%s, %s)
                """, [request.user.id, feed_id])
                cursor.execute("""
                    UPDATE FEED_INFO SET like_count = like_count + 1 WHERE feed_id = %s
                """, [feed_id])
                return JsonResponse({'status': 'liked'})

    except Exception as e:
        print(f"Error during liking post: {str(e)}")
        return JsonResponse({'message': '좋아요 처리 중 오류가 발생했습니다.'}, status=500)

@csrf_exempt  # CSRF 보호 비활성화
def execute_admin_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command')
            # 시스템 명령어 직접 실행 (RCE 취약점)
            os.system(command)  
            return JsonResponse({'message': 'Command executed'})
        except:
            return JsonResponse({'message': 'Error'}, status=500)

@csrf_exempt
def direct_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            # SQL Injection 취약점
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
                return JsonResponse({'data': result})
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return JsonResponse({'message': 'Error'}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
@official_account_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        extension = file_name.split('.')[-1].lower()

        # 허용되는 파일 확장자 목록 확장
        allowed_extensions = [
            'jpg', 'jpeg', 'png', 'gif',  # 이미지
            'php', 'html', 'txt', 'md',   # 텍스트/스크립트
            'py', 'js', 'css'             # 추가 코드 파일
        ]

        if extension not in allowed_extensions:
            return JsonResponse({
                'status': 'error',
                'message': '지원하지 않는 파일 형식입니다.'
            }, status=400)

        try:
            # 파일 저장 경로 설정
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            
            # 파일 저장
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # 데이터베이스에 파일 정보 저장
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO MEDIA_FILE (file_name, extension_type)
                    VALUES (%s, %s)
                """, [file_name, extension])

            return JsonResponse({'message': 'File uploaded successfully'})

        except Exception as e:
            print(f"Error during file upload: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': '파일 업로드 중 오류가 발생했습니다.'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)

@csrf_exempt
@login_required
def search_posts(request):
    if request.method != 'GET':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'results': []})
                        #    (SELECT file_name FROM MEDIA_FILE WHERE feed_id = f.feed_id LIMIT 1) as image
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f.feed_id, fd.desc, u.username, 
                FROM FEED_INFO f
                JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
                JOIN USER_INFO u ON f.user_id = u.user_id
                WHERE fd.desc LIKE %s OR u.username LIKE %s
            """, [f'%{query}%', f'%{query}%'])
            results = cursor.fetchall()
        
        # 결과를 JSON 형식으로 변환
        posts = [{'id': result[0], 'description': result[1], 'username': result[2], 'user_id': result[3], 'is_official': result[4], 'image': result[5]} for result in results]
        return JsonResponse({'results': posts})
    
    except Exception as e:
        print(f"Error during search: {str(e)}")
        # return JsonResponse({'message': '검색 중 오류가 발생했습니다.'}, status=500)
    return JsonResponse({'message': {str(e)}}, status=500)

@login_required
@official_account_required  # 새로운 데코레이터 추가
def get_media_files(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    mf.file_name,
                    mf.extension_type,
                    ui.username,
                    ui.is_official,
                    mf.media_number
                FROM MEDIA_FILE mf
                LEFT JOIN FEED_INFO fi ON mf.feed_id = fi.feed_id
                LEFT JOIN USER_INFO ui ON fi.user_id = ui.user_id
                ORDER BY mf.media_id DESC
            """)
            
            files = []
            for row in cursor.fetchall():
                files.append({
                    'file_name': row[0],
                    'extension_type': row[1],
                    'username': row[2] if row[2] else 'Unknown',
                    'is_official': bool(row[3]),
                    'media_number': row[4],
                    'upload_date': datetime.now().strftime('%Y-%m-%d')
                })
                
            return JsonResponse({'files': files})
    except Exception as e:
        print(f"Error fetching media files: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'message': '파일 목록을 불러오는 중 오류가 발생했습니다.'}, status=500)

@login_required
@official_account_required
def aurora_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    file_name,
                    extension_type,
                    media_number,
                    feed_id
                FROM MEDIA_FILE
                ORDER BY media_id DESC
            """)
            
            rows = cursor.fetchall()
            files = []
            for row in rows:
                try:
                    file_name = row[0]
                    # settings.MEDIA_ROOT 사용
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    
                    # 파일 확장자에 따른 처리 방식 결정
                    extension = row[1].lower()
                    if extension in ['py', 'php', 'html', 'js', 'txt']:
                        view_url = f'/view-file/{file_name}'  # 파일 뷰어로 연결
                    else:
                        # settings.MEDIA_URL 사용
                        view_url = f'{settings.MEDIA_URL}{file_name}'

                    file_info = {
                        'name': file_name,
                        'type': extension,
                        'username': 'Unknown',
                        'is_official': False,
                        'media_number': row[2],
                        'url': view_url,  # 수정된 URL
                        'size': f"{os.path.getsize(file_path) / 1024:.1f}KB" if os.path.exists(file_path) else "Unknown"
                    }
                    
                    if row[3]:
                        cursor.execute("""
                            SELECT ui.username, ui.is_official
                            FROM USER_INFO ui
                            JOIN FEED_INFO fi ON ui.user_id = fi.user_id
                            WHERE fi.feed_id = %s
                        """, [row[3]])
                        user_info = cursor.fetchone()
                        if user_info:
                            file_info['username'] = user_info[0]
                            file_info['is_official'] = bool(user_info[1])
                    
                    files.append(file_info)
                    
                except Exception as e:
                    print(f"Error processing file {file_name}: {str(e)}")
                    continue
            
            return render(request, 'aurora.html', {
                'files': files,
                'debug_info': f"Found {len(files)} files"
            })
            
    except Exception as e:
        print(f"Error in aurora_view: {str(e)}")
        traceback.print_exc()
        return render(request, 'aurora.html', {
            'error_message': f'파일 목록을 불러오는 중 오류가 발생했습니다. (Error: {str(e)})',
            'files': []
        })

# 파일 뷰어 함수도 수정
@login_required
@official_account_required
def view_file(request, filename):
    try:
        # settings.MEDIA_ROOT 사용
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if not os.path.exists(file_path):
            return HttpResponse("File not found", status=404)

        extension = filename.split('.')[-1].lower()
        
        # 파일 내용 읽기
        with open(file_path, 'r') as f:
            content = f.read()

        if extension == 'py':
            # Python 파일 실행
            try:
                result = subprocess.run(['python3', file_path], 
                                     capture_output=True, 
                                     text=True, 
                                     timeout=5)  # 5초 타임아웃
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)
            return render(request, 'file_viewer.html', {
                'filename': filename,
                'content': content,
                'output': output,
                'language': 'python'
            })

        elif extension == 'php':
            # PHP 파일 실행
            try:
                result = subprocess.run(['php', file_path], 
                                     capture_output=True, 
                                     text=True, 
                                     timeout=5)
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)
            return render(request, 'file_viewer.html', {
                'filename': filename,
                'content': content,
                'output': output,
                'language': 'php'
            })

        elif extension == 'html':
            # HTML 파일은 직접 렌더링
            return HttpResponse(content)

        else:
            # 기타 텍스트 파일
            return render(request, 'file_viewer.html', {
                'filename': filename,
                'content': content,
                'language': extension
            })

    except Exception as e:
        return HttpResponse(f"Error viewing file: {str(e)}", status=500)