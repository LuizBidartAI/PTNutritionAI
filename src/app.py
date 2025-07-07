"""
Main application entry point for PTNutritionAI
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ptnutrition.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Main application route"""
    return {
        "message": "Welcome to PTNutritionAI!",
        "status": "Application is running",
        "version": "0.1.0"
    }

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PTNutritionAI"}

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
