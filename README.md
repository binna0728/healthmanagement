# 건강 관리 CLI 프로젝트

## 프로젝트 개요
- 개인의 키, 몸무게, 메모를 기록하고 BMI를 계산해 주는 콘솔 기반 건강 관리 프로그램입니다.
- MySQL 8.0을 데이터베이스로 사용하며 Docker Compose 또는 로컬 MySQL 환경에서 쉽게 실행할 수 있도록 구성되어 있습니다.
- `health_management/health_manager.py`는 프로그램의 메인 진입점으로, CRUD 기능과 BMI 계산 로직을 제공합니다.

## 주요 기능
- 건강 기록 추가, 조회, 수정, 삭제 기능 제공
- 입력한 키와 몸무게를 활용한 BMI 자동 계산 및 분류
- Docker Compose와 Makefile을 통한 개발 환경 자동화 (컨테이너 실행, 초기 데이터베이스 셋업 등)

## 폴더 구조
```
.
├── docker-compose.yaml        # 루트에서 사용하는 MySQL Compose (필요 시)
├── health_management/
│   ├── health_manager.py      # 메인 애플리케이션
│   ├── docker-compose.yaml    # 건강 관리 앱 전용 Compose
│   ├── init_health.sql        # health_db 스키마 및 테이블 생성 스크립트
│   ├── Makefile               # Docker/MySQL/앱 실행 관련 명령 모음
│   └── requirements.txt       # 파이썬 의존성 목록
└── README.md
```

## 빠른 시작
### 1. 환경 준비
- Python 3.10+
- pip
- Docker 및 Docker Compose

### 2. 가상환경 및 패키지 설치
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r health_management\requirements.txt
```

### 3. Docker로 데이터베이스 실행 (권장)
```powershell
cd health_management
docker-compose up -d
```

### 4. 데이터베이스 초기화
```powershell
cd health_management
docker-compose exec mysql mysql -uroot -p1234 -e "SOURCE /docker-entrypoint-initdb.d/init_health.sql;"
```
- 또는 Makefile을 사용할 경우:
```powershell
cd health_management
make db-start
make db-init
```

### 5. 애플리케이션 실행
```powershell
cd health_management
python health_manager.py
```
- Makefile 단축 명령:
```powershell
cd health_management
make run
```

## 수동(MySQL 직접 설치) 실행 절차
1. 로컬에 MySQL 8.0 설치 후 `health_db` 데이터베이스 생성
2. `init_health.sql`을 실행하여 `health_records` 테이블을 생성
3. `.env` 또는 코드 내 접속 정보(`host`, `port`, `user`, `password`)를 실제 환경에 맞게 수정
4. 가상환경을 활성화하고 `python health_manager.py` 실행

## 유용한 Makefile 명령
```text
make install   # requirements.txt 기반 의존성 설치
make setup     # 패키지를 editable 모드로 설치하여 'myhealth' 명령 사용 가능
make db-start  # Docker 기반 MySQL 컨테이너 실행
make db-stop   # 컨테이너 중지
make db-status # 컨테이너 및 DB 상태 확인
make db-init   # health_db 초기화 및 테이블 생성
make run       # 애플리케이션 실행
make clean     # 컨테이너와 볼륨 정리 (주의)
```

## 참고 사항
- 기본 MySQL 접속 정보는 `host=localhost`, `port=3307`, `user=root`, `password=1234`, `database=health_db` 입니다.
- Docker 버전을 사용할 경우 `health_management/docker-compose.yaml`이 해당 포트와 환경 변수를 설정합니다.
- `Makefile` 명령은 Linux/macOS, Windows(WSL/MinGW) 환경에서 사용 가능합니다. PowerShell에서는 `make` 대신 `python`, `docker-compose` 명령을 직접 실행하세요.
