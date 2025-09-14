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

import math

@app.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not query:
        return jsonify({"results": [], "current_page": 1, "total_pages": 1})

    conn = get_db_connection()
    cursor = conn.cursor()

    search_term = f"%{query}%"

    # First, get the total count of matching results
    count_cursor = conn.cursor()
    count_cursor.execute('''
        SELECT COUNT(*)
        FROM pages
        WHERE title LIKE ? OR body LIKE ? OR description LIKE ? OR keywords LIKE ?
    ''', (search_term, search_term, search_term, search_term))
    total_results = count_cursor.fetchone()[0]

    # Calculate total pages
    total_pages = math.ceil(total_results / per_page) if total_results > 0 else 1

    # Ensure current page is within valid range
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    # Calculate offset for pagination
    offset = (page - 1) * per_page

    # Fetch results for the current page
    cursor.execute('''
        SELECT url, title, body, description, keywords
        FROM pages
        WHERE title LIKE ? OR body LIKE ? OR description LIKE ? OR keywords LIKE ?
        LIMIT ? OFFSET ?
    ''', (search_term, search_term, search_term, search_term, per_page, offset))

    results = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries for JSON serialization
    results_list = []
    for row in results:
        results_list.append(dict(row))
    
    return jsonify({
        "results": results_list,
        "current_page": page,
        "total_pages": total_pages
    })

if __name__ == '__main__':
    app.run(debug=True)
