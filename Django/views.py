from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import bcrypt

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
