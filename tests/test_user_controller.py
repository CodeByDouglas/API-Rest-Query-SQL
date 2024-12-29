import pytest
from app import create_app
from unittest.mock import patch
from tests.utils import limpar_email_de_teste

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

#TESTES CONSULTA POR ID
def test_get_user_existente_ID(client):

    response= client.get('api/users/id/1')
    responseBody= response.get_json()
    assert response.status_code == 200

    assert responseBody["id"] == 1
    assert responseBody["name"] == "User1"
    assert responseBody["email"] == "user1@example.com"


def test_get_user_naoencontrado_ID(client):

    response= client.get('api/users/id/9999')
    responseBody= response.get_json()
    assert response.status_code == 404
    assert "message" in responseBody
    assert responseBody["message"] == "User not found"

def test_get_user_errodeconexao_ID(client):

    with patch("app.services.user_service.get_db_connection", side_effect=Exception("Database connection error")):

        response= client.get('api/users/id/1')
        responseBody= response.get_json()
        assert response.status_code == 500
    
        assert "message" in responseBody
        assert responseBody["message"] == "Internal server error"

#TEST DE CONSULTA POR E-MAIL
def test_get_user_existente_Email(client):

    response= client.get('api/users/email/user1@example.com')
    responseBody= response.get_json()
    assert response.status_code == 200

    assert responseBody["id"] == 1
    assert responseBody["name"] == "User1"
    assert responseBody["email"] == "user1@example.com"


def test_get_user_naoencontrado_Email(client):

    response= client.get('api/users/email/user9999@example.com')
    responseBody= response.get_json()
    assert response.status_code == 404
    assert "message" in responseBody
    assert responseBody["message"] == "User not found"

def test_get_user_errodeconexao_Email(client):

    with patch("app.services.user_service.get_db_connection", side_effect=Exception("Database connection error")):

        response= client.get('api/users/email/user1@example.com')
        responseBody= response.get_json()
        assert response.status_code == 500
    
        assert "message" in responseBody
        assert responseBody["message"] == "Internal server error"

#TEST DE CONSULTA POR USER NAME
def test_get_user_existente_UserName(client):

    response= client.get('api/users/username/User1')
    responseBody= response.get_json()
    assert response.status_code == 200

    assert responseBody["id"] == 1
    assert responseBody["name"] == "User1"
    assert responseBody["email"] == "user1@example.com"


def test_get_user_naoencontrado_UserName(client):

    response= client.get('api/users/username/User9999')
    responseBody= response.get_json()
    assert response.status_code == 404
    assert "message" in responseBody
    assert responseBody["message"] == "User not found"

def test_get_user_errodeconexao_UserName(client):

    with patch("app.services.user_service.get_db_connection", side_effect=Exception("Database connection error")):

        response= client.get('api/users/username/User1')
        responseBody= response.get_json()
        assert response.status_code == 500
    
        assert "message" in responseBody
        assert responseBody["message"] == "Internal server error"

#Apaga os E-mails utilizados pelo tests
@pytest.fixture(autouse=True)
def limpar_dados_de_teste():
    limpar_email_de_teste("newuser@example.com")
    

def test_add_user(client):

    response =  client.post('api/users/add', json={
        "name": "New User",
        "email": "newuser@example.com"
        })
    responseBody = response.get_json()
    
    assert response.status_code == 201
    assert responseBody["id"] is not None
    assert responseBody["name"] == "New User"
    assert responseBody["email"] == "newuser@example.com"
    assert responseBody["message"] == "User successfully created"

def test_add_user_existente(client):
    
    response = client.post('api/users/add', json={
        "name": "New User", 
        "email": "user1@example.com"
    })

    responseBody = response.get_json()
    
    assert response.status_code == 409
    assert responseBody["message"] == "User already exists"


def test_add_user_db_error(client):
    with patch("app.controllers.user_controller.adicionar_user_ao_db", side_effect=Exception("Database connection error")):
        response = client.post('/api/users/add', json={
            "name": "New User",
            "email": "newuser@example.com"
        })
        responseBody = response.get_json()

        assert response.status_code == 500
        assert responseBody["message"] == "Internal server error"