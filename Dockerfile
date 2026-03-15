# CheckVisa SelfVisa - Dockerfile
# Python 3.11 with LibreOffice

FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (단계별)
# 1. apt 업데이트
RUN apt-get update

# 2. LibreOffice 설치
RUN apt-get install -y --no-install-recommends \
        libreoffice-writer \
        libreoffice-calc \
        libreoffice-common

# 3. 한글 폰트 설치
RUN apt-get install -y --no-install-recommends \
        fonts-nanum \
        fonts-nanum-coding \
        fontconfig

# 4. 폰트 캐시 갱신 및 정리
RUN fc-cache -f -v && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# selfvisa 폴더 전체 복사
COPY selfvisa/ .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 설정
EXPOSE 5000

# gunicorn으로 실행
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120"]
