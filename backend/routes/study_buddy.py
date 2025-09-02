from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.database import get_db
from utils.huggingface_api import generate_flashcards

study_bp = Blueprint('study', __name__)

@study_bp.route('/flashcards', methods=['POST'])
def create_flashcards():
    data = request.json
    notes = data.get('notes')
    
    if not notes:
        return jsonify({'error': 'Study notes are required'}), 400
    
    # Generate flashcards
    flashcards = generate_flashcards(notes)
    
    # Store in database
    db = get_db()
    saved_cards = []
    
    for card in flashcards:
        flashcard_data = {
            'question': card['question'],
            'answer': card['answer'],
            'created_at': datetime.utcnow().isoformat()
        }
        result = db.table('flashcards').insert(flashcard_data).execute()
        if result.data:
            saved_cards.append(result.data[0])
    
    return jsonify({
        'message': f'Created {len(saved_cards)} flashcards',
        'flashcards': saved_cards
    })

@study_bp.route('/flashcards', methods=['GET'])
def get_flashcards():
    db = get_db()
    result = db.table('flashcards').select('*').order('created_at', desc=True).execute()
    return jsonify(result.data)