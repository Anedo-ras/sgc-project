from flask import Blueprint, current_app, request, jsonify
from datetime import datetime
from utils.database import get_db
from utils.huggingface_api import analyze_sentiment
import mysql.connector

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/entry', methods=['POST'])
def add_mood_entry():
    data = request.json
    journal_text = data.get('text')
    
    if not journal_text:
        return jsonify({'error': 'Journal text is required'}), 400
    
    # Analyze sentiment
    sentiment = analyze_sentiment(journal_text)
    
    # Store in database
    db = get_db(current_app._get_current_object())
    
    if hasattr(db, 'cursor'):  # MySQL connection
        try:
            cursor = db.cursor()
            query = "INSERT INTO mood_entries (text, sentiment, score) VALUES (%s, %s, %s)"
            values = (journal_text, sentiment['label'], sentiment['score'])
            cursor.execute(query, values)
            db.commit()
            
            entry_id = cursor.lastrowid
            cursor.close()
            
            return jsonify({
                'message': 'Entry saved successfully',
                'sentiment': sentiment,
                'entry_id': entry_id
            })
        except mysql.connector.Error as e:
            return jsonify({'error': f'Database error: {e}'}), 500
    else:  # Supabase
        entry = {
            'text': journal_text,
            'sentiment': sentiment['label'],
            'score': sentiment['score'],
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = db.table('mood_entries').insert(entry).execute()
        
        return jsonify({
            'message': 'Entry saved successfully',
            'sentiment': sentiment,
            'entry_id': result.data[0]['id'] if result.data else None
        })

@mood_bp.route('/entries', methods=['GET'])
def get_mood_entries():
    db = get_db(current_app._get_current_object())
    
    if hasattr(db, 'cursor'):  # MySQL connection
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM mood_entries ORDER BY created_at DESC")
            entries = cursor.fetchall()
            cursor.close()
            
            return jsonify(entries)
        except mysql.connector.Error as e:
            return jsonify({'error': f'Database error: {e}'}), 500
    else:  # Supabase
        result = db.table('mood_entries').select('*').order('created_at', desc=True).execute()
        return jsonify(result.data)

@mood_bp.route('/stats', methods=['GET'])
def get_mood_stats():
    db = get_db(current_app._get_current_object())
    
    if hasattr(db, 'cursor'):  # MySQL connection
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT sentiment, score, created_at FROM mood_entries")
            stats = cursor.fetchall()
            cursor.close()
            
            return jsonify(stats)
        except mysql.connector.Error as e:
            return jsonify({'error': f'Database error: {e}'}), 500
    else:  # Supabase
        result = db.table('mood_entries').select('sentiment, score, created_at').execute()
        return jsonify(result.data)