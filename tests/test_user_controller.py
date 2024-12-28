import pytest
from app import create_app
from datetime import datetime

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


