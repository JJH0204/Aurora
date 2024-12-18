김지홍
gimjihong3618
온라인

최민제 — 24. 12. 11. 오후 9:58
오 넵
정재호 — 24. 12. 12. 오전 9:07
@장진영 AWS VPC 방화벽 끄셔야돼여 
돈나가요
정재호 — 24. 12. 12. 오전 9:36
@장진영 @장진영
정재호 — 24. 12. 12. 오후 2:40
docker run -d --name aurora -p 80:80 -v "$(pwd)/Aurora:/app/Aurora" krjaeh0/aurora:latest
김범준 — 24. 12. 12. 오후 3:08
이미지
김범준 — 24. 12. 12. 오후 3:17
이미지
색 있는 부분은 구축해야 하는 요구사항입니다
정재호 — 24. 12. 12. 오후 10:18
첨부 파일 형식: acrobat
청구서 _ Billing and Cost Management _ Global.pdf
254.64 KB
시간 괜찮으시면 aws 들어가 보세요 저도 혹시나 해서 들어가 봤는데 지운다고 지워도 요금이 계속 부가되고 있었어요...
@everyone
장진영 — 24. 12. 12. 오후 10:24
보고 들어갔더니 저도 방화벽때문에
7달러 나왓네요...
정재호 — 24. 12. 12. 오후 10:24
분명 오전까지는 3달러였는데
..
장진영 — 24. 12. 12. 오후 10:25
어디서 끄는지도 모르겟네요
정재호 — 24. 12. 12. 오후 10:25
리전 별로 요금이 책정되여
VPC EC2 들어가셔서 방화벽 삭제하고 머신 삭제하면 되는데
저는 그렇게 해도 요금이 계속 나와서
걍 계정을 삭제했습니다
장진영 — 24. 12. 12. 오후 10:29
아 오늘 오전에 제로요금 메일설정한거 왔었네요...
정재호 — 24. 12. 12. 오후 10:31
몸은 좀 괜찮으신가요?
장진영 — 24. 12. 12. 오후 10:31
복대차고있습니다...
물리치료받고..
정재호 — 24. 12. 12. 오후 10:32
저런...
장진영 — 24. 12. 12. 오후 10:34
삭제해야하나 firewall들어가면 시작하기말고
뭐 만든게없는데
전 딱 1만원 청구되겠네요...
김범준 — 24. 12. 13. 오전 12:27
엇....아 이ㄹ아다우아 전 8달러네요 아아아이런
정재호 — 24. 12. 13. 오전 12:38
동지...
김범준 — 24. 12. 13. 오전 12:40
10.26 달러가 되었네요 ㅎㅎ하..
정재호 — 24. 12. 13. 오전 1:35
오...
동지인 줄알았는데..
난 호상이구나
정재호 — 24. 12. 13. 오후 3:50
이미지
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane     # Control Plane 노드
  extraPortMappings:
  - containerPort: 80     # Kubernetes 서비스의 포트
확장
cluster-config.yaml
1KB
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aurora-deployment
spec:
  replicas: 1
확장
aurora-deployment.yaml
1KB
apiVersion: v1
kind: Service
metadata:
  name: aurora-service
spec:
  selector:
확장
aurora-service.yaml
1KB
첨부 파일 형식: acrobat
1.kubernetes_in_windows.pdf
165.58 KB
첨부 파일 형식: acrobat
2.Kubernetes-on-dockerImage.pdf
175.84 KB
김범준 — 24. 12. 13. 오후 5:48
kubectl port-forward --address 0.0.0.0 pod/aurora-deployment-5c54fc85d7-bmtns 80:80
정재호 — 24. 12. 16. 오전 10:14
이미지
최민제 — 24. 12. 16. 오전 10:42
샘플 오피셜 
-> 닉네임 이메일 , 마크 
어드민 페이지 
-> DB 출력 , 이즈 오피셜 수정 가능하게 
프로필 페이지 
-> 프록시 > 이즈 오피셜 나오는지 확인
오피셜 계정이면 모든파일 올리기 가능
정재호 — 24. 12. 16. 오전 10:50
Django admin 페이지에서 관리자 계정을 만드는 방법은 아래와 같아! 이 과정은 superuser(슈퍼유저) 계정을 생성하는 것을 의미하고, 관리자 권한을 가진 계정을 생성하는 데 사용돼. 

---

가상환경 활성화
Django 프로젝트가 실행 중인 가상환경을 활성화해야 해.

source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows


---

Django 프로젝트 디렉토리로 이동
manage.py 파일이 있는 디렉토리로 이동해.

cd 프로젝트_폴더_경로


---

superuser 생성 명령 실행
Django의 createsuperuser 명령을 사용해서 관리자 계정을 생성해.

python manage.py createsuperuser


---

관리자 정보 입력
명령을 실행하면 아래와 같이 정보 입력을 요구해:

Username (leave blank to use 'your_username'): admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.


Username: 원하는 사용자 이름 (보통 admin 사용)
Email address: 관리자의 이메일 주소
Password: 관리자가 사용할 비밀번호 입력 (2번 입력)

---

서버 실행 후 관리자 페이지 접속
Django 개발 서버를 실행해서 관리자 페이지에 접속해.

python manage.py runserver


관리자 페이지 URL은 기본적으로 다음과 같아:
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

생성한 username과 password로 로그인하면 Django Admin 페이지에 접근할 수 있어!

---

관리자 페이지 설정 확인
프로젝트의 settings.py 파일에서 INSTALLED_APPS에 django.contrib.admin이 활성화돼 있는지 확인.
migrate가 적용되지 않았다면 먼저 아래 명령으로 데이터베이스 마이그레이션 실행:

python manage.py migrate


---

이렇게 하면 Django Admin에서 사용할 관리자 계정을 만들 수 있어! 😄
장진영 — 24. 12. 16. 오전 11:12
웹쉘 or 쉘 얻는 경로
admin 계정 탈취 -> 로그인 창에서 ID: admin@aurora.com 입력 후 비밀번호 입력 시, 패스워드가 잘못됐다는 alert -> 히드라로 탈취
프로필 편집 -> proxy intercept시에 isOfficial 변수 수정시 본인 계정이 official 계정으로 업그레이드 -> official 계정은 php 업로드 가능
Admin 페이지 -> admin  페이지에서는 USER_INFO 테이블을 보고 수정가능 -> 본인의 계정의 isOfficial 수정하여 본인 계정을 직접 official 계정으로 업그레이드
 
김지홍 — 24. 12. 16. 오전 11:13
데이터베이스 및 모델 관리 모듈
django.db: 데이터베이스 ORM(Object-Relational Mapping) 기능을 제공합니다.
django.db.models: 데이터베이스 모델 정의를 지원합니다.
django.db.migrations: 데이터베이스 마이그레이션 관리 도구입니다.
장진영 — 24. 12. 16. 오전 11:42
ToDoList
Edit Profile 에 기본적으로 본인의 메일, 닉네임, 바이오 정보 입력된상태로 출력 (해결)
-> 현재 공백으로 초기화되어있어서 유저가 닉네임만 수정후 Save하게되면 Email값이 공백으로 변경되어 로그인이 안됨 
김범준 — 24. 12. 16. 오후 3:06
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
확장
kind-config.yaml
1KB
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
확장
aurora-deployment.yaml
1KB
apiVersion: v1
kind: Service
metadata:
  name: aurora-service
spec:
  selector:
확장
aurora-service.yaml
1KB
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane     # Control Plane 노드
  extraPortMappings:
  - containerPort: 80     # Kubernetes 서비스의 포트
확장
cluster-config.yaml
1KB
노윤서 — 어제 오후 3:48
이미지
정재호 — 오늘 오전 11:13
이미지
이미지
이미지
장진영 — 오늘 오전 11:53
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
확장
message.txt
25KB
정재호 — 오늘 오전 11:53
import os
import subprocess

def main():
    print("Python Web Shell")
    print("================")
    print("1. Execute Python code")
    print("2. Run shell command")
    print("3. Exit")
    print("================")

    while True:
        choice = input("Choose an option (1/2/3): ")
        if choice == '1':
            execute_python_code()
        elif choice == '2':
            run_shell_command()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

def execute_python_code():
    print("\n[ Execute Python Code ]")
    try:
        code = input("Enter Python code to execute:\n>>> ")
        exec(code)  # 위험한 코드 실행
    except Exception as e:
        print(f"Error: {e}")

def run_shell_command():
    print("\n[ Run Shell Command ]")
    try:
        command = input("Enter shell command to run:\n$ ")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Output:\n{result.stdout}")
        print(f"Error:\n{result.stderr}")
    except Exception as e:
        print(f"Error: {e}")

if name == "main":
    main()
﻿
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
                    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
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
                f.feed_type
            FROM FEED_INFO f
            LEFT JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
            LEFT JOIN USER_INFO ui ON f.user_id = ui.user_id
            LEFT JOIN RankedMedia rm ON f.feed_id = rm.feed_id AND rm.rn = 1
            ORDER BY f.feed_id DESC;
        """)
        
        columns = [col[0] for col in cursor.description]
        feeds = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # 로그인한 사용자의 좋아요 상태 확인
        like_post = set()
        if request.user.is_authenticated:
            cursor.execute("""
                SELECT feed_id FROM FEED_LIKE WHERE user_id = %s
            """, [request.user.id])
            like_post = {row[0] for row in cursor.fetchall()}
        
        for feed in feeds:
            feed['isLiked'] = feed['feed_id'] in like_post
            
            # 각 게시물의 모든 미디어 파일 가져오기
            cursor.execute("""
                SELECT file_name, extension_type
                FROM MEDIA_FILE
                WHERE feed_id = %s
            """, [feed['feed_id']])
            media_files = cursor.fetchall()
            feed['media_files'] = [{'file_name': file[0], 'extension_type': file[1]} for file in media_files]
            feed['profile_image'] = f"/media/{feed['profile_image']}" if feed['profile_image'] else '/static/img/default_profile.png'
        
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
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        # 파일 확장자/타입 검사 없이 저장 (파일 업로드 취약점)
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return JsonResponse({'message': 'File uploaded'})

@csrf_exempt
@login_required
def search_posts(request):
    if request.method != 'GET':
        return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)

    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'results': []})
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT f.feed_id, fd.desc, u.username, 
                       (SELECT file_name FROM MEDIA_FILE WHERE feed_id = f.feed_id LIMIT 1) as image
                FROM FEED_INFO f
                JOIN FEED_DESC fd ON f.feed_id = fd.feed_id
                JOIN USER_INFO u ON f.user_id = u.user_id
                WHERE fd.desc LIKE %s OR u.username LIKE %s
            """, [f'%{query}%', f'%{query}%'])
            results = cursor.fetchall()
        
        # 결과를 JSON 형식으로 변환
        posts = [{'id': result[0], 'description': result[1], 'username': result[2], 'image': result[3]} for result in results]
        return JsonResponse({'results': posts})
    
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return JsonResponse({'message': '검색 중 오류가 발생했습니다.'}, status=500)

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
message.txt
25KB