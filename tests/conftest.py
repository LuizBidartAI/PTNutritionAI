"""
Test configuration and utilities for PTNutritionAI
"""

import pytest
from src.app import app, db

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def runner():
    """Create a test runner for the Flask application."""
    return app.test_cli_runner()
