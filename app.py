#!/usr/bin/env python3
"""
Foundation Dashboard Flask Application
Interactive web application for exploring foundation AI research data
"""

from flask import Flask, render_template, jsonify, request
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.foundation_loader import FoundationDataLoader
from data.chat_service import FoundationChatService

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Initialize data loader and chat service
data_loader = FoundationDataLoader()
chat_service = None  # Initialize lazily when first chat request is made

@app.route('/')
def dashboard():
    """Main dashboard page with filtering interface"""
    # Load taxonomy options for filters
    taxonomy_data = data_loader.get_taxonomy_options()
    foundation_count = data_loader.get_foundation_count()
    
    return render_template('dashboard.html', 
                         taxonomy_data=taxonomy_data,
                         foundation_count=foundation_count)

@app.route('/foundation/<string:foundation_name>')
def foundation_detail(foundation_name):
    """Individual foundation detail page"""
    foundation = data_loader.get_foundation_by_name(foundation_name)
    if not foundation:
        return "Foundation not found", 404
    
    return render_template('foundation_detail.html', foundation=foundation)

@app.route('/api/foundations')
def api_foundations():
    """API endpoint to get foundations with optional filtering"""
    filters = {}
    
    # Extract filter parameters from request
    for key in request.args:
        if key == 'search':
            filters['search'] = request.args.get('search', '')
        elif key == 'ai_readiness_min':
            filters['ai_readiness_min'] = int(request.args.get('ai_readiness_min', 0))
        elif key == 'ai_readiness_max':
            filters['ai_readiness_max'] = int(request.args.get('ai_readiness_max', 10))
        else:
            # Handle taxonomy filters (can be multiple values)
            values = request.args.getlist(key)
            if values:
                filters[key] = values
    
    foundations = data_loader.get_filtered_foundations(filters)
    stats = data_loader.get_filtered_statistics(foundations)
    
    return jsonify({
        'foundations': foundations,
        'stats': stats,
        'total_count': len(foundations)
    })

@app.route('/api/foundation/<string:foundation_name>')
def api_foundation_detail(foundation_name):
    """API endpoint for individual foundation data"""
    foundation = data_loader.get_foundation_by_name(foundation_name)
    if not foundation:
        return jsonify({'error': 'Foundation not found'}), 404
    
    return jsonify(foundation)

@app.route('/api/stats')
def api_stats():
    """API endpoint for overall statistics"""
    return jsonify(data_loader.get_overall_statistics())

@app.route('/api/taxonomy')
def api_taxonomy():
    """API endpoint for taxonomy options"""
    return jsonify(data_loader.get_taxonomy_options())

@app.route('/chat')
def chat_interface():
    """Chat interface page"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for processing natural language queries"""
    global chat_service
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Initialize chat service lazily
        if chat_service is None:
            try:
                chat_service = FoundationChatService()
            except ValueError as e:
                return jsonify({'error': str(e)}), 500
        
        # Process query using map-reduce approach
        import asyncio
        result = asyncio.run(chat_service.process_query(query))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500

if __name__ == '__main__':
    # Create necessary directories
    Path('templates').mkdir(exist_ok=True)
    Path('static/css').mkdir(parents=True, exist_ok=True)
    Path('static/js').mkdir(parents=True, exist_ok=True)
    Path('data').mkdir(exist_ok=True)

    # Use PORT from environment (required for Render.com) or default to 6001
    port = int(os.environ.get('PORT', 6001))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'

    app.run(debug=debug, host='0.0.0.0', port=port)