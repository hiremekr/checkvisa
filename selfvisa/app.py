"""
CheckVisa SelfVisa - Flask 서버
통합신청서 PDF 자동 생성 서비스
"""
from flask import Flask, send_from_directory, request, jsonify, send_file
from flask_cors import CORS
import os
import io
import sys

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.dirname(__file__))

from pdf_generator import fill_form

app = Flask(__name__)

# CORS 설정 - checkvisa.co.kr에서 API 호출 가능하게
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://checkvisa.co.kr",
            "http://localhost:*",
            "http://127.0.0.1:*"
        ]
    }
})

# 루트 경로
@app.route('/')
def index():
    """메인 페이지"""
    return send_from_directory('.', 'index.html')

# 정적 파일 (CSS, JS, 이미지 등)
@app.route('/<path:filename>')
def static_files(filename):
    """정적 파일 서빙"""
    return send_from_directory('.', filename)

# API - PDF 생성
@app.route('/api/generate-pdf', methods=['POST', 'OPTIONS'])
def generate_pdf():
    """통합신청서 PDF 생성 API"""
    
    # CORS preflight 처리
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # JSON 데이터 받기
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({'error': '데이터가 없습니다.'}), 400
        
        # PDF 생성
        print(f"[INFO] PDF 생성 시작: {data.get('surname', 'Unknown')}")
        pdf_bytes = fill_form(data)
        print(f"[INFO] PDF 생성 완료: {len(pdf_bytes)} bytes")
        
        # PDF 파일로 반환
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='통합신청서.pdf'
        )
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"[ERROR] PDF 생성 실패:\n{error_detail}")
        
        return jsonify({
            'error': str(e),
            'detail': error_detail
        }), 500

# Health check
@app.route('/health')
def health():
    """서버 상태 확인"""
    return jsonify({
        'status': 'ok',
        'service': 'checkvisa-selfvisa',
        'version': '1.0.0'
    })

# 개발 서버 실행
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print('=' * 60)
    print('🚀 CheckVisa SelfVisa 서버 시작')
    print('=' * 60)
    print(f'포트: {port}')
    print(f'디버그: {debug}')
    print('=' * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
