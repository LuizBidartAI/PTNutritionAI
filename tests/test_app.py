"""
Basic tests for the PTNutritionAI application
"""

def test_index_route(client):
    """Test the main index route."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Welcome to PTNutritionAI!"
    assert data['status'] == "Application is running"

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"
    assert data['service'] == "PTNutritionAI"
