FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# curl 설치 (이미지 용량 최소화)
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 pip 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app 디렉토리 복사
COPY app ./app

# 포트 8000 노출
EXPOSE 8000

# FastAPI 실행 (app.py 사용)
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
