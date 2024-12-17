# Aurora Project
> Team Firewalls. N LED Team. First Collaboration Project. 2024.12.10  
> 두 팀이 가진 폭발적인 에너지를 오로라 처럼 아름답게 표현하자.

## 목차

* [프로젝트 개요](#project-overview)
* [기술 스택](#technology-stack)
* [프로젝트 구조](#project-structure)
* [프로젝트 플로우-차트](#project-flowchart)
* [프로젝트 실행 방법](#how-to-run-project)
* [보안 구성](#security-configuration)
* [라이선스](#license)

## Project Overview

Aurora는 사이버 보안 교육을 위한 취약한 웹 애플리케이션 플랫폼입니다.  
Django 웹 프레임워크를 기반으로 하며, MariaDB를 데이터베이스로 사용하고 Docker를 통해 컨테이너화되어 있습니다.

### 🎯 프로젝트 목표

| 주요 목표 | 세부 내용 |
|---------|----------|
| **보안 학습 환경 구축** | • 의도적으로 취약한 웹 서버 구축<br>• 실제 공격/방어 시나리오 체험<br>• 웹 개발 보안 취약점 실습 |
| **보안 도구 개발** | • 공격 탐지 시스템 구현<br>• 방어 솔루션 구축<br>• 로그 모니터링 시스템 개발 |
| **실무 역량 강화** | • 보안 문서 작성 능력 향상<br>• 문제 해결 능력 개발<br>• 팀 협업 경험 |

### 🏆 해킹 방어 대회 (2024.12.20)

| 구분 | 세부 내용 |
|-----|----------|
| **웹 서버** | • 최소 10개 이상의 취약점 포함 |
| **모바일 앱(선택)** | • 취약한 안드로이드 앱 개발<br>• 게임 또는 유틸리티 앱 |
| **보안 시스템** | • 침입 탐지 시스템<br>• 로그 수집/분석 시스템<br>• 보안관제 솔루션 |

| 대회 진행 정보 | 내용 |
|--------------|------|
| **참가 팀** | Firewall-LED(7명) vs NIS-Caffeine(7명) |
| **승리 조건** | Root 권한 또는 Root Shell 획득 |
| **진행 방식** | 실시간 공격/방어 동시 진행 |

## technology-stack
| 구분 | 기술 |
|------|------|
| Frontend | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript) |
| Backend | ![Django](https://img.shields.io/badge/Django-5.0-green?logo=django) |
| Database | ![MariaDB](https://img.shields.io/badge/MariaDB-10.11-blue?logo=mariadb) |
| Container | ![Docker](https://img.shields.io/badge/Docker-Latest-blue?logo=docker) |
| Web Server | ![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2-green?logo=gunicorn) |
| Security | ![ModSecurity](https://img.shields.io/badge/ModSecurity-3.0-red?logo=modsecurity) ![Suricata](https://img.shields.io/badge/Suricata-7.0-orange) ![ELK Stack](https://img.shields.io/badge/ELK_Stack-7.17-blue?logo=elastic) |
| Orchestration | ![Kubernetes](https://img.shields.io/badge/Kubernetes-Latest-blue?logo=kubernetes) |

## project-structure
```
Aurora/
├── Aurora/               # → Django 프로젝트 메인 디렉토리(프런트)
├── Django/               # → Django 애플리케이션 디렉토리(서버)
├── Maria/                # → MariaDB 관련 설정(데이터베이스)
├── Kubernetes/           # → Kubernetes 배포 설정
│   ├── Security/        # → 보안 모니터링 구성
│   │   ├── elk/        # → ELK 스택 설정
│   │   └── monitoring/ # → Suricata, Filebeat 설정
├── .github/              # → GitHub 워크플로우 설정
├── manage.py             # → Django 프로젝트 관리
├── requirements.txt      # → Python 의존성
├── Dockerfile           # → Docker 이미지 정의
├── docker-entrypoint.sh # → Docker 진입점 스크립트
├── run.bat              # → Windows 실행 스크립트
└── run.sh               # → Linux/Mac 실행 스크립트
```

## how-to-run-project
### 1. 로컬 개발 환경
```bash
$ git clone <repository-url>
$ cd Aurora
$ ./run.bat  # Windows
# 또는 ./run.sh (Linux/Mac)
```

### 2. Docker 환경
```bash
# 기본 실행
$ docker run -d --name aurora -p 80:80 krjaeh0/aurora:latest

# (선택사항) 소스코드 실시간 반영
$ docker run -d --name aurora -p 80:80 -v "%cd%/Aurora:/app/Aurora" krjaeh0/aurora:latest
```

### 3. Kubernetes 환경
```bash
# 1. 기본 애플리케이션 배포
$ cd Kubernetes
$ ./deploy.bat  # Windows
# 또는 ./deploy.sh (Linux/Mac)

# 2. 보안 모니터링 시스템 배포
$ cd Security
$ ./deploy-security.bat  # Windows
# 또는 ./deploy-security.sh (Linux/Mac)
```

### 4. 접속 정보
- 웹 애플리케이션: http://localhost
- 관리자 페이지: http://localhost/admin
- Kibana 대시보드: http://localhost:30601

## Security Configuration

### 1. WAF (ModSecurity)
- 웹 애플리케이션 방화벽이 기본으로 활성화되어 있음
- OWASP Core Rule Set (CRS) 적용
- 로그 확인:
```bash
# Docker 환경
docker exec aurora tail -f /var/log/modsec_audit.log

# Kubernetes 환경
kubectl exec <pod-name> -- tail -f /var/log/modsec_audit.log
```

### 2. 네트워크 모니터링 (Suricata)
- 네트워크 침입 탐지/방지 시스템 (IDS/IPS)
- 실시간 트래픽 분석 및 위협 탐지
- 모든 보안 이벤트는 ELK 스택으로 전송됨

### 3. 로그 수집 및 분석 (ELK Stack)
- Elasticsearch: 로그 저장 및 검색
- Logstash: 로그 수집 및 변환
- Kibana: 로그 시각화 및 분석
- 접속 정보:
  - URL: http://localhost:30601
  - 사용자: elastic
  - 비밀번호: 환경 변수에서 설정 (기본값: `choa0306@@`)

### 4. 보안 모범 사례
- 모든 비밀번호와 API 키는 Kubernetes Secrets로 관리
- 컨테이너는 최소 권한 원칙으로 실행
- 정기적인 보안 업데이트 및 패치 적용
- 모든 통신은 TLS/SSL로 암호화

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.