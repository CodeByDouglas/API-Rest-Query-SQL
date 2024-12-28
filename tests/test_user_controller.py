import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def client():
    app = create_app()  
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_status_database(client): 

    response= client.get('/api/Status_database')
    
    assert response.status_code == 200

    responseBody = response.get_json()
    assert "status" in responseBody
    assert responseBody["status"] == "success"
    
    assert "Active_connections" in responseBody
    active_connections = int(responseBody["Active_connections"])
    assert 1 <= active_connections <= 100
    
    assert "Current Date" in responseBody
    assert responseBody["Current Date"] is not None
    
    assert "DB Version" in responseBody
    assert responseBody["DB Version"] == "PostgreSQL 15.10 (Debian 15.10-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit"
    
    assert "Max Connections" in responseBody
    assert responseBody["Max Connections"] == 100

def test_get_user_existente(client):

    response= client.get('api/user/1')
    responseBody= response.get_json()
    assert response.status_code == 200

    assert responseBody["id"] == 1
    assert responseBody["name"] == "User1"
    assert responseBody["email"] == "user1@example.com"


def test_get_user_naoencontrado(client):

    response= client.get('api/user/9999')
    responseBody= response.get_json()
    assert response.status_code == 404
    assert "message" in responseBody
    assert responseBody["message"] == "User not found"

def test_get_user_errodeconexao(client):

    with patch("app.config.get_db_connection", side_effect=Exception("Database connection error")):
        response= client.get('api/user/1')
        responseBody= response.get_json()
        assert response.status_code == 500
    
        assert "message" in responseBody
        assert responseBody["message"] == "Internal server error"
    
