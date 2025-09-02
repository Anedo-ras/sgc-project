from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.database import get_db
from utils.openai_api import get_recipe_suggestions

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/suggest', methods=['POST'])
def suggest_recipes():
    data = request.json
    ingredients = data.get('ingredients', [])
    
    if not ingredients:
        return jsonify({'error': 'At least one ingredient is required'}), 400
    
    # Get recipe suggestions
    recipes = get_recipe_suggestions(ingredients)
    
    # Store in database
    db = get_db()
    saved_recipes = []
    
    for recipe in recipes:
        recipe_data = {
            'name': recipe['name'],
            'ingredients': recipe['ingredients'],
            'instructions': recipe['instructions'],
            'created_at': datetime.utcnow().isoformat()
        }
        result = db.table('recipes').insert(recipe_data).execute()
        if result.data:
            saved_recipes.append(result.data[0])
    
    return jsonify({
        'message': f'Found {len(saved_recipes)} recipes',
        'recipes': saved_recipes
    })

@recipe_bp.route('/recipes', methods=['GET'])
def get_recipes():
    db = get_db()
    result = db.table('recipes').select('*').order('created_at', desc=True).execute()
    return jsonify(result.data)