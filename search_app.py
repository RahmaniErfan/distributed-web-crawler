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
    # Fetch all matching results to apply weighting
    cursor.execute('''
        SELECT url, title, body, description, keywords
        FROM pages
        WHERE title LIKE ? OR body LIKE ? OR description LIKE ? OR keywords LIKE ?
    ''', (search_term, search_term, search_term, search_term))
    all_results = cursor.fetchall()
    conn.close()

    # Apply weighting: prioritize title matches
    weighted_results = []
    for row in all_results:
        score = 0
        if row['title'] and query.lower() in row['title'].lower():
            score += 10 # Higher score for title matches
        if row['body'] and query.lower() in row['body'].lower():
            score += 1 # Lower score for body matches
        if row['description'] and query.lower() in row['description'].lower():
            score += 5 # Medium score for description matches
        if row['keywords'] and query.lower() in row['keywords'].lower():
            score += 3 # Medium score for keyword matches
        weighted_results.append({"row": dict(row), "score": score})

    # Sort results by score in descending order
    weighted_results.sort(key=lambda x: x['score'], reverse=True)

    # Extract only the rows after sorting
    sorted_results = [item['row'] for item in weighted_results]

    total_results = len(sorted_results)
    total_pages = math.ceil(total_results / per_page) if total_results > 0 else 1

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page
    paginated_results = sorted_results[offset:offset + per_page]
    
    return jsonify({
        "results": paginated_results,
        "current_page": page,
        "total_pages": total_pages
    })

if __name__ == '__main__':
    app.run(debug=True)
