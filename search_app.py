import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import os
app = Flask(__name__,
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app) # Enable CORS for all routes

DATABASE = 'scraped_data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor()

    # Basic full-text search using LIKE.
    # For more advanced search, consider integrating with a dedicated search engine (e.g., Whoosh, Elasticsearch)
    # or SQLite's FTS5 extension.
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT url, title, body, description, keywords
        FROM pages
        WHERE title LIKE ? OR body LIKE ? OR description LIKE ? OR keywords LIKE ?
        LIMIT 50
    ''', (search_term, search_term, search_term, search_term))

    results = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries for JSON serialization
    results_list = []
    for row in results:
        results_list.append(dict(row))
    
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)
