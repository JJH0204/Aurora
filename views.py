@login_required
@official_account_required
def view_file(request, filename):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if not os.path.exists(file_path):
            return HttpResponse("File not found", status=404)

        extension = filename.split('.')[-1].lower()
        
        # 파일 내용 읽기
        with open(file_path, 'r') as f:
            content = f.read()

        # Python 또는 PHP 파일인 경우 직접 실행
        if extension in ['py', 'php']:
            try:
                if extension == 'py':
                    # Python 파일 직접 실행
                    result = subprocess.run(['python3', file_path], 
                                         capture_output=True, 
                                         text=True,
                                         timeout=5)  # 5초 타임아웃
                else:
                    # PHP 파일 직접 실행
                    result = subprocess.run(['php', file_path], 
                                         capture_output=True, 
                                         text=True,
                                         timeout=5)
                
                output = result.stdout + result.stderr
                
                # 실행 결과와 소스 코드를 함께 표시
                return render(request, 'file_viewer.html', {
                    'filename': filename,
                    'content': content,
                    'output': output,
                    'language': extension
                })
            except subprocess.TimeoutExpired:
                return HttpResponse("실행 시간이 초과되었습니다.", status=500)
            except Exception as e:
                return HttpResponse(f"실행 오류: {str(e)}", status=500)

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