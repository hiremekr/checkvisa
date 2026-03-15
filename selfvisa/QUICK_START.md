# 🚀 CheckVisa SelfVisa - 배포 완료 체크리스트

## ✅ 완료된 작업

1. **Python Flask 서버 구현 완료** ✅
   - 파일: `selfvisa/app.py`
   - 통합신청서 PDF 생성 API
   - CORS 설정 (checkvisa.co.kr 허용)
   - Health check 엔드포인트

2. **배포 설정 파일 작성 완료** ✅
   - `requirements.txt`: Python 패키지
   - `Procfile`: Heroku/Railway용
   - `railway.json`: Railway 설정
   - `nixpacks.toml`: LibreOffice 자동 설치
   - `DEPLOYMENT.md`: 배포 가이드

3. **GitHub 푸시 완료** ✅
   - 저장소: https://github.com/hiremekr/checkvisa
   - 커밋: 8538bbf

4. **로컬 테스트 완료** ✅
   - PDF 생성 성공: 58,473 bytes
   - Health check 작동
   - CORS 작동

---

## 🎯 다음 단계 (배포하기)

### 방법 1: Railway (추천, 빠름) ⚡

**소요 시간**: 10분

1. **Railway 계정 만들기**
   - 사이트: https://railway.app
   - GitHub 계정으로 로그인

2. **새 프로젝트 생성**
   ```
   New Project → Deploy from GitHub repo
   → hiremekr/checkvisa 선택
   ```

3. **설정**
   ```
   Root Directory: selfvisa
   (다른 설정은 자동)
   ```

4. **배포**
   - "Deploy" 클릭
   - 5-10분 대기
   - URL 받기: `https://xxxxx.up.railway.app`

5. **테스트**
   ```bash
   curl https://xxxxx.up.railway.app/health
   ```

---

### 방법 2: Render (무료, 신용카드 불필요) 💳

**소요 시간**: 15분

1. **Render 계정 만들기**
   - 사이트: https://render.com
   - GitHub 계정으로 로그인

2. **새 Web Service 생성**
   ```
   New + → Web Service
   → GitHub 저장소 연결: hiremekr/checkvisa
   ```

3. **설정 입력**
   ```
   Name: checkvisa-selfvisa
   Root Directory: selfvisa
   Runtime: Python 3
   
   Build Command:
   apt-get update && apt-get install -y libreoffice-writer --no-install-recommends && pip install -r requirements.txt
   
   Start Command:
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   
   Plan: Free
   ```

4. **환경 변수** (선택)
   ```
   PORT=10000
   DEBUG=false
   ```

5. **배포**
   - "Create Web Service" 클릭
   - 10-15분 대기
   - URL 받기: `https://checkvisa-selfvisa.onrender.com`

6. **테스트**
   ```bash
   curl https://checkvisa-selfvisa.onrender.com/health
   ```

⚠️ **Render 무료 티어 주의**:
- 15분 비활성 시 서버 슬립
- 첫 요청 시 30-60초 소요
- → "PDF 생성 중... 최대 1분 소요" 안내 필요

---

## 🔗 프론트엔드 연결하기

배포 완료 후 받은 URL을 프론트엔드에 연결합니다.

### checkvisa.co.kr/selfvisa/index.html 수정

1. **API URL 설정 추가** (파일 상단 스크립트에)

```javascript
// ============================================
// API 설정
// ============================================
const SELFVISA_API_URL = 'https://your-app.up.railway.app/api/generate-pdf';
// 또는
// const SELFVISA_API_URL = 'https://checkvisa-selfvisa.onrender.com/api/generate-pdf';
```

2. **generateIntegratedForm 함수 수정** (약 1299번째 줄)

현재 코드:
```javascript
async function generateIntegratedForm() {
    const data = { /* 데이터 수집 */ };
    
    // 기존: 서버 API 호출 (상대 경로)
    const response = await fetch('/selfvisa/api/generate-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    // ...
}
```

변경:
```javascript
async function generateIntegratedForm() {
    const data = {
        application_type: getApplicationType(),
        surname: document.getElementById('surnameEn').value,
        given_names: document.getElementById('givenNameEn').value,
        birth_year: document.getElementById('birthYear').value,
        birth_month: document.getElementById('birthMonth').value,
        birth_day: document.getElementById('birthDay').value,
        sex: document.querySelector('input[name="gender"]:checked')?.value || '',
        nationality: document.getElementById('nationality').value,
        alien_reg_no: `${document.getElementById('birthYear').value}${document.getElementById('birthMonth').value}${document.getElementById('birthDay').value}-${document.getElementById('alienRegNum2').value}`,
        passport_no: document.getElementById('passportNum').value,
        passport_issue: document.getElementById('passportIssue').value,
        passport_expiry: document.getElementById('passportExpiry').value,
        address_korea: document.getElementById('addressKorea').value,
        phone: document.getElementById('phoneKorea').value,
        cell_phone: document.getElementById('cellPhone').value,
        address_home: document.getElementById('addressHome').value || '',
        phone_home: document.getElementById('phoneHome').value || '',
        application_date: document.getElementById('applicationDate').value,
        application_purpose: document.getElementById('applicationPurpose').value || ''
    };
    
    // 변경: 배포된 API URL 사용
    const response = await fetch(SELFVISA_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'PDF 생성 실패');
    }
    
    const blob = await response.blob();
    return await blob.arrayBuffer();
}
```

3. **Git 커밋 & 푸시**
```bash
git add selfvisa/index.html
git commit -m "feat: SelfVisa API URL 연결 (Railway 배포 서버)"
git push origin main
```

---

## 🧪 최종 테스트

### 1. API 서버 테스트
```bash
# Health check
curl https://your-app.up.railway.app/health

# PDF 생성 테스트
curl -X POST https://your-app.up.railway.app/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"application_type":"체류기간연장허가","surname":"KIM","given_names":"CHUL SOO","birth_year":"1990","birth_month":"01","birth_day":"01","sex":"남","nationality":"VIETNAM","alien_reg_no":"900101-1234567","passport_no":"M12345678","passport_issue":"2020-01-01","passport_expiry":"2030-01-01","address_korea":"서울시","phone":"02-1234-5678","cell_phone":"010-1234-5678","address_home":"Home","phone_home":"+84-123","application_date":"2026-03-15"}' \
  -o test.pdf
```

### 2. 웹사이트 테스트
1. https://checkvisa.co.kr/selfvisa/ 접속
2. 데이터 입력
3. 통합신청서 체크
4. "PDF 생성하기" 클릭
5. PDF 다운로드 확인

### 3. 모바일 테스트
1. 스마트폰으로 접속
2. 데이터 입력
3. PDF 생성
4. 다운로드 확인

---

## 📊 예상 비용

| 플랫폼 | 월 비용 | 성능 |
|--------|--------|------|
| **Railway** | $3-5 | ⚡⚡⚡ 빠름 |
| **Render (Free)** | $0 | ⚡ 느림 (첫 로드 30초) |

---

## 🐛 문제 해결

### 405 오류 (Method Not Allowed)
→ API URL이 올바른지 확인

### 500 오류 (Internal Server Error)
→ Railway/Render 로그 확인

### CORS 오류
→ API 서버의 CORS 설정 확인

### PDF 생성 타임아웃
→ gunicorn timeout 늘리기 (railway.json 수정)

---

## 📞 도움이 필요하면

1. **Railway 로그 확인**
   - Railway 대시보드 → Logs 탭

2. **Render 로그 확인**
   - Render 대시보드 → Logs 탭

3. **API 테스트**
   ```bash
   curl -v https://your-app/health
   ```

---

## ✅ 최종 체크리스트

배포 완료 전 확인:

- [ ] Railway/Render에 배포 완료
- [ ] Health check 작동 (`/health`)
- [ ] PDF 생성 테스트 성공
- [ ] 프론트엔드 API URL 연결
- [ ] 데스크탑 테스트 완료
- [ ] 모바일 테스트 완료
- [ ] 405 오류 해결

모두 체크되면 **배포 완료!** 🎉
