# 라이브러리 목록 생성 명령어

pip list --format=freeze > requirements.txt

# 가상환경 생성및 활성화 명령어

python -m venv venv
venv\Scripts\activate

# 라이브러리 목록 파일토대로 의존성 주입 명령어

pip install -r requirements.txt

# fast api 실행 명령어

uvicorn main:app --host 0.0.0.0 --port 8000
