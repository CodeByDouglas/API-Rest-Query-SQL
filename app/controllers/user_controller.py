from flask import Blueprint, jsonify, request
from app.config import get_db_connection
from app.services.user_service import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/Status_database', methods=['GET'])
def test_db():
    try:
        database_connection = get_db_connection()
        cursor_execucao = database_connection.cursor()
        
        cursor_execucao.execute("SELECT setting FROM pg_settings WHERE name = 'max_connections';")
        max_connections = cursor_execucao.fetchone()[0]

        cursor_execucao.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE datname = current_database();")
        active_connections = cursor_execucao.fetchone()[0]
        
        cursor_execucao.execute("SELECT NOW();")
        date = cursor_execucao.fetchone()[0]
        
        cursor_execucao.execute("SELECT version();")
        db_version = cursor_execucao.fetchone()[0]
        
        
        database_connection.close()
        
        return jsonify({
            "status": "success",
            "Active_connections": active_connections,
            "Current Date": str(date), 
            "DB Version": db_version,
            "Max Connections": int(max_connections)}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@user_bp.route('/users/id/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    try: 

        user= buscar_user_por_id(user_id)

        if user: 
            return jsonify({
                "id": user[0],
                "name": user[1],
                "email": user[2]
                }), 200
        else: 
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e: 
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


@user_bp.route('/users/email/<string:user_email>', methods=['GET'])
def get_user_email(user_email):
    try: 

        user= buscar_user_por_email(user_email)

        if user: 
            return jsonify({
                "id": user[0],
                "name": user[1],
                "email": user[2]
                }), 200
        else: 
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e: 
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


@user_bp.route('/users/username/<string:user_username>', methods=['GET'])
def get_user_username(user_username):
    try: 

        user= buscar_user_por_userName(user_username)

        if user: 
            return jsonify({
                "id": user[0],
                "name": user[1],
                "email": user[2]
                }), 200
        else: 
            return jsonify({"message": "User not found"}), 404
    
    except Exception as e: 
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

@user_bp.route('/users/add', methods=['POST'])
def add_user():
    try: 
        dados = request.get_json()
        name = dados.get("name")
        email = dados.get("email")

        is_valid, error_message = validar_dados_user(name, email)
        if not is_valid:
            return jsonify({"message": error_message}), 400
        
        if verificar_user_exite(email): 
            return  jsonify({"message": "User already exists"}), 409
        
        user_id = adicionar_user_ao_db(name, email)

        return jsonify({
            "id": user_id,
            "name": name,
            "email": email,
            "message": "User successfully created"}), 201
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500