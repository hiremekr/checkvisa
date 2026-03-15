# CheckVisa SelfVisa - 출입국 통합신청서 자동작성

## 📋 개요
출입국관리법 시행규칙 별지 제34호 서식(통합신청서/신고서)을 자동으로 생성하는 웹 서비스입니다.

## 🎯 주요 기능
- ✅ 통합신청서(신고서) 자동 작성 및 PDF 생성
- ✅ 거주숙소제공확인서 생성 (클라이언트 사이드)
- ✅ 신원보증서 생성 (클라이언트 사이드)
- ✅ E-7-4 점수 자동 계산
- ✅ localStorage 자동 저장

## 📁 파일 구조
```
selfvisa/
├── index.html                  # 메인 페이지 (사용자 인터페이스)
├── pdf_generator.py            # PDF 생성 핵심 로직
├── routes.py                   # Flask Blueprint (백엔드용)
├── __init__.py                 # 패키지 초기화
├── templates/
│   └── selfvisa_form.html     # HTML 템플릿
└── assets/
    └── 통합신청서(신고서).doc  # Word 템플릿 (필수!)
```

## 🚀 배포 방법

### 방법 1: 정적 사이트 (Cloudflare Pages)
현재 구조 그대로 사용:
- `/selfvisa/` 접속 시 `index.html` 제공
- PDF 생성은 클라이언트에서 직접 처리 (제한적)

### 방법 2: Flask 백엔드 추가 (권장)
Python 백엔드 서버 필요:

1. **Flask 앱에 통합**:
```python
# app.py 또는 main.py
from selfvisa.routes import selfvisa_bp
app.register_blueprint(selfvisa_bp, url_prefix='/selfvisa')
```

2. **필수 패키지 설치**:
```bash
pip install python-docx>=0.8.11 pypdf>=4.0 lxml>=4.9
```

3. **LibreOffice 설치** (PDF 변환에 필수):
```bash
# Ubuntu/Debian
sudo apt-get update && apt-get install -y libreoffice --no-install-recommends

# Dockerfile
RUN apt-get update && apt-get install -y \
    libreoffice \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
```

4. **서버 실행**:
```bash
python app.py
```

5. **접속**:
- 폼 페이지: `http://localhost:5000/selfvisa/`
- PDF 생성 API: `POST http://localhost:5000/selfvisa/api/generate-pdf`

## 🔧 API 스펙

### POST /selfvisa/api/generate-pdf

**Request Body (JSON)**:
```json
{
    "application_type": "extension",
    "surname": "NGUYEN",
    "given_names": "VAN AN",
    "birth_year": "1992",
    "birth_month": "03",
    "birth_day": "20",
    "sex": "M",
    "nationality": "VIETNAM",
    "alien_reg_no": "920320-5123456",
    "passport_no": "B12345678",
    "passport_issue": "2020-01-01",
    "passport_expiry": "2030-01-01",
    "address_korea": "서울특별시 강남구 테헤란로 123",
    "phone": "02-1234-5678",
    "cell_phone": "010-1234-5678",
    "application_date": "2026년 03월 15일"
}
```

**Response**: PDF 파일 (`application/pdf`, ~54KB)

## ⚠️ 주의사항
1. **LibreOffice 필수**: PDF 변환에 반드시 필요
2. **Word 템플릿**: `assets/통합신청서(신고서).doc` 파일 필수
3. **처리 시간**: 2~10초 (LibreOffice 변환 포함)
4. **Python 3.8+**: python-docx 호환성

## 📝 개발 참고사항
- 통합신청서는 서버사이드 생성 (python-docx + LibreOffice)
- 거주숙소확인서/신원보증서는 클라이언트사이드 생성 (PDF-lib)
- Word 템플릿 수정 시 행 높이 조정 필요 (`pdf_generator.py`의 `ROW_HEIGHTS`)

## 🔗 관련 링크
- [출입국관리법 시행규칙 별지 제34호](https://www.law.go.kr)
- [python-docx 문서](https://python-docx.readthedocs.io/)
- [pypdf 문서](https://pypdf.readthedocs.io/)

---

© 2026 CheckVisa - E-7-4 비자 신청 서류 자동작성
