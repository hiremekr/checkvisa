"""
selfvisa Flask Blueprint
기존 Flask app.py에 아래 한 줄 추가:
    from selfvisa.routes import selfvisa_bp
    app.register_blueprint(selfvisa_bp, url_prefix='/selfvisa')
"""
import io
from flask import Blueprint, request, jsonify, send_file, send_from_directory
import os

selfvisa_bp = Blueprint(
    'selfvisa', __name__,
    template_folder='templates',
    static_folder='static'
)

# pdf_generator.py 경로 설정 (같은 디렉토리에 배치했다고 가정)
from .pdf_generator import fill_form


@selfvisa_bp.route('/')
@selfvisa_bp.route('')
def index():
    """셀프비자 폼 페이지"""
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), 'templates'),
        'selfvisa_form.html'
    )


@selfvisa_bp.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """JSON 데이터를 받아 통합신청서 PDF 반환"""
    data = request.get_json(force=True)
    try:
        pdf_bytes = fill_form(data)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='통합신청서.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@selfvisa_bp.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'selfvisa'})
