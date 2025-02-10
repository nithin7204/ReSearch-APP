from flask import render_template, jsonify, request
from app import app, cache
from app.services.research_service import ResearchService
from app.services.ai_service import AIService

research_service = ResearchService()
ai_service = AIService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
@cache.memoize(timeout=300)
def search():
    query = request.args.get('query', '')
    source = request.args.get('source', 'all')
    
    if not query:
        return jsonify({'results': [], 'message': 'Please provide a search query'})
    
    try:
        results = research_service.search(query, source)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    if not data or 'abstract' not in data:
        return jsonify({'error': 'Abstract is required'}), 400
    
    try:
        summary = ai_service.generate_summary(data['abstract'])
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview():
    data = request.json
    if not data or 'title' not in data or 'abstract' not in data:
        return jsonify({'error': 'Title and abstract are required'}), 400
    
    try:
        preview = ai_service.generate_preview(data['title'], data['abstract'])
        return jsonify({'preview': preview})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
