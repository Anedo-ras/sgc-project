import os
import supabase
from flask import current_app
import mysql.connector
from mysql.connector import Error

def init_db(app):
    db_type = os.getenv('DATABASE_TYPE', 'supabase').lower()
    
    if db_type == 'mysql':
        # Initialize MySQL connection
        try:
            connection = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
            
            if connection.is_connected():
                app.mysql_connection = connection
                print("MySQL database connection established")
                
                # Initialize tables if they don't exist
                init_mysql_tables(connection)
                
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            raise
    else:
        # Initialize Supabase client
        try:
            client = supabase.create_client(
                app.config['SUPABASE_URL'],
                app.config['SUPABASE_KEY']
            )
            app.supabase = client
            print("Supabase connection established")
        except Exception as e:
            print(f"Error connecting to Supabase: {e}")
            raise

def init_mysql_tables(connection):
    """Create tables if they don't exist"""
    try:
        cursor = connection.cursor()
        
        # Mood Journal table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                text TEXT NOT NULL,
                sentiment VARCHAR(20),
                score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Study Buddy table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Recipe Recommender table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                ingredients TEXT,
                instructions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table for future authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128),
                is_premium BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        connection.commit()
        print("MySQL tables initialized successfully")
        
    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if cursor:
            cursor.close()

def get_db(app):
    if hasattr(app, 'mysql_connection'):
        return app.mysql_connection
    elif hasattr(app, 'supabase'):
        return app.supabase
    else:
        raise Exception("No database connection established")

def close_db(app):
    if hasattr(app, 'mysql_connection') and app.mysql_connection.is_connected():
        app.mysql_connection.close()
        print("MySQL connection closed")