from flask import Blueprint, jsonify
from app.config import get_db_connection

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
            "Active_connections": active_connections,
            "Current Date": str(date), 
            "DB Version": db_version,
            "Max Connections": int(max_connections)}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
