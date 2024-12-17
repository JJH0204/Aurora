# Security Monitoring Setup for Kubernetes

이 디렉토리는 Kubernetes 클러스터의 보안 모니터링을 위한 설정 파일들을 포함하고 있습니다.

## 디렉토리 구조
```
Security/
├── deploy-security.bat    # 전체 배포 스크립트
├── elk/                   # ELK 스택 관련 설정
│   ├── elk-namespace.yaml
│   ├── elasticsearch.yaml
│   └── kibana.yaml
└── monitoring/           # 모니터링 구성요소 설정
    ├── monitoring-namespace.yaml
    ├── elasticsearch-secret.yaml
    ├── suricata-config.yaml
    ├── suricata-daemonset.yaml
    ├── filebeat-config.yaml
    └── filebeat-daemonset.yaml
```

## 설치 방법

1. 배포 스크립트 실행:
```bash
cd Security
deploy-security.bat
```

2. 설치 완료 후 접속 정보:
- Kibana 대시보드: http://localhost:30601
- 기본 계정:
  - 사용자명: elastic
  - 비밀번호: changeme

## 주요 구성요소

1. ELK 스택
- Elasticsearch: 로그 저장 및 검색 엔진
- Kibana: 로그 시각화 및 분석 도구

2. 모니터링 도구
- Suricata: 네트워크 트래픽 모니터링 및 위협 탐지
- Filebeat: 로그 수집 및 전송

## 주의사항

1. 보안
- 기본 비밀번호는 반드시 변경하여 사용하세요
- 프로덕션 환경에서는 적절한 보안 설정이 필요합니다

2. 스토리지
- 현재 설정은 임시 스토리지(emptyDir)를 사용합니다
- 프로덕션 환경에서는 영구 볼륨(PV)을 사용해야 합니다

3. 리소스
- Elasticsearch는 기본적으로 512MB의 메모리를 사용하도록 설정되어 있습니다
- 필요에 따라 리소스 설정을 조정하세요
