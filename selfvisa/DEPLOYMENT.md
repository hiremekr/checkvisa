# CheckVisa SelfVisa - 배포 가이드

## 🚀 Railway에 배포하기 (무료, 추천)

### 1단계: Railway 계정 생성
1. https://railway.app 접속
2. GitHub 계정으로 로그인

### 2단계: 새 프로젝트 생성
1. "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. `hiremekr/checkvisa` 저장소 선택

### 3단계: 설정
1. Root Directory: `/selfvisa` 입력 (중요!)
2. Build Command: 자동 감지됨 (nixpacks.toml 사용)
3. Start Command: 자동 감지됨 (gunicorn)

### 4단계: 환경 변수 (선택)
```
PORT=5000
DEBUG=false
```

### 5단계: 배포
- "Deploy" 클릭
- 5-10분 대기
- 배포 완료 후 URL 받기: `https://xxxxx.up.railway.app`

### 6단계: 프론트엔드 연결
`checkvisa.co.kr/selfvisa/index.html` 파일에서:

```javascript
// 기존
const API_URL = '/selfvisa/api/generate-pdf';

// 변경
const API_URL = 'https://xxxxx.up.railway.app/api/generate-pdf';
```

---

## 📊 배포 플랫폼 비교

| 플랫폼 | 무료 티어 | 장점 | 단점 |
|--------|----------|------|------|
| **Railway** | 월 $5 크레딧 | 쉬움, 빠름 | 신용카드 필요 |
| **Render** | 750시간/월 | 신용카드 불필요 | 느림 (첫 로드 30초) |
| **Heroku** | 없음 | - | 유료 전환 |
| **Vercel** | 무제한 | 매우 빠름 | Python 제한적 |

---

## 🔧 Render에 배포하기 (완전 무료, 신용카드 불필요)

### 1단계: Render 계정 생성
1. https://render.com 접속
2. GitHub 계정으로 로그인

### 2단계: 새 Web Service 생성
1. "New +" → "Web Service" 클릭
2. GitHub 저장소 연결: `hiremekr/checkvisa`

### 3단계: 설정
```
Name: checkvisa-selfvisa
Root Directory: selfvisa
Runtime: Python 3
Build Command: apt-get update && apt-get install -y libreoffice-writer --no-install-recommends && pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 4단계: 환경 변수
```
PORT=10000
DEBUG=false
```

### 5단계: Plan 선택
- "Free" 선택 (무료)
- "Create Web Service" 클릭

### 6단계: 배포 대기
- 첫 배포: 10-15분 소요
- URL 받기: `https://checkvisa-selfvisa.onrender.com`

### ⚠️ Render 무료 티어 주의사항
- 15분간 요청이 없으면 서버가 슬립 모드로 전환
- 슬립 모드에서 깨어나는데 30-60초 소요
- 해결: 첫 로드 시 "PDF 생성 중... 최대 1분 소요" 안내 표시

---

## 🌐 프론트엔드 연결하기

배포 완료 후 받은 URL을 프론트엔드에 연결합니다.

### selfvisa/index.html 수정

```javascript
// 파일 상단에 API URL 설정
const SELFVISA_API_URL = 'https://your-app.up.railway.app/api/generate-pdf';
// 또는
// const SELFVISA_API_URL = 'https://checkvisa-selfvisa.onrender.com/api/generate-pdf';

// generateIntegratedForm 함수 수정
async function generateIntegratedForm() {
    const data = {
        application_type: getApplicationType(),
        surname: document.getElementById('surnameEn').value,
        given_names: document.getElementById('givenNameEn').value,
        // ... 나머지 필드
    };

    // API 호출
    const response = await fetch(SELFVISA_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error('PDF 생성 실패');
    }

    const blob = await response.blob();
    return await blob.arrayBuffer();
}
```

---

## 🧪 테스트하기

### 1. Health Check
```bash
curl https://your-app.up.railway.app/health
```

예상 응답:
```json
{
  "status": "ok",
  "service": "checkvisa-selfvisa",
  "version": "1.0.0"
}
```

### 2. PDF 생성 테스트
```bash
curl -X POST https://your-app.up.railway.app/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "application_type": "체류자격외활동허가",
    "surname": "KIM",
    "given_names": "CHUL SOO",
    "birth_year": "1990",
    "birth_month": "01",
    "birth_day": "01",
    "sex": "남",
    "nationality": "VIETNAM",
    "alien_reg_no": "900101-1234567",
    "passport_no": "M12345678",
    "passport_issue": "2020-01-01",
    "passport_expiry": "2030-01-01",
    "address_korea": "서울특별시 강남구",
    "phone": "02-1234-5678",
    "cell_phone": "010-1234-5678",
    "address_home": "123 Street, City",
    "phone_home": "+84-123-456-789",
    "application_date": "2026-03-15"
  }' \
  -o test.pdf

# 확인
file test.pdf
# 출력: test.pdf: PDF document, version 1.6
```

---

## 💰 비용

### Railway
- **무료 티어**: 월 $5 크레딧 (500MB RAM, 500MB 디스크)
- 예상 사용량: 월 $3-5
- **추천**: 소규모 프로젝트

### Render
- **완전 무료**: 750시간/월 (512MB RAM)
- 제한: 슬립 모드 (15분 비활성 시)
- **추천**: 예산이 빡빡한 경우

---

## 🔒 보안

### CORS 설정
현재 설정:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://checkvisa.co.kr"]
    }
})
```

### Rate Limiting (선택)
Flask-Limiter 사용:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour"]
)
```

---

## 📞 문제 해결

### LibreOffice 설치 실패
```bash
# railway.json 또는 nixpacks.toml 확인
# apt-get 명령어가 올바른지 확인
```

### 타임아웃 오류
```python
# gunicorn timeout 늘리기
gunicorn app:app --timeout 300
```

### 메모리 부족
```python
# workers 수 줄이기
gunicorn app:app --workers 1
```

---

## 🎯 다음 단계

1. ✅ Railway 또는 Render에 배포
2. ✅ API URL 받기
3. ✅ 프론트엔드(checkvisa.co.kr)에 API URL 연결
4. ✅ 테스트
5. ✅ 사용자에게 공개

---

## 📚 참고 링크

- [Railway 문서](https://docs.railway.app/)
- [Render 문서](https://render.com/docs)
- [Flask 문서](https://flask.palletsprojects.com/)
- [Gunicorn 문서](https://docs.gunicorn.org/)
