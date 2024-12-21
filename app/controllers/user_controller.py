from flask import Blueprint, jsonify
from app.config import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/Status_database', methods=['GET'])
def test_db():
    try:
        database_connection = get_db_connection()
        cursor_execucao = database_connection.cursor()
        cursor_execucao.execute("SELECT 1")
        result = cursor_execucao.fetchone()
        database_connection.close()
        
        return jsonify({"status": "success", "result": result}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
