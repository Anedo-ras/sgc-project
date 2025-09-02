from django.apps import apps
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from utils.database import init_db
from routes.mood_journal import mood_bp
from routes.study_buddy import study_bp
from routes.recipe_recommender import recipe_bp
apps.config['MYSQL_HOST'] = 'localhost'
apps.config['MYSQL_USER'] = 'your_username'
apps.config['MYSQL_PASSWORD'] = 'your_password'
apps.config['MYSQL_DB'] = 'your_database_name'
apps.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app = Flask(__name__, 
           static_folder='../frontend',
           template_folder='../frontend/templates')
app.config.from_object(Config)

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(mood_bp, url_prefix='/api/mood')
app.register_blueprint(study_bp, url_prefix='/api/study')
app.register_blueprint(recipe_bp, url_prefix='/api/recipe')

CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mood')
def mood_journal():
    return render_template('mood.html')

@app.route('/study')
def study_buddy():
    return render_template('study.html')

@app.route('/recipes')
def recipe_recommender():
    return render_template('recipes.html')

if __name__ == '__main__':
    app.run(debug=True)