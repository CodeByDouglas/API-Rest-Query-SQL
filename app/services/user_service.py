from app.config import get_db_connection

def buscar_user_por_id(user_id): 
    try: 
        database_connection= get_db_connection()
        cursor_execucao= database_connection.cursor()

        cursor_execucao.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))

        user= cursor_execucao.fetchone()
        database_connection.close()

        return user
    except Exception as e: 
        raise Exception(f"Database error: {str(e)}")

def buscar_user_por_email(user_email): 
    try: 
        database_connection= get_db_connection()
        cursor_execucao= database_connection.cursor()

        cursor_execucao.execute("SELECT id, name, email FROM users WHERE email = %s", (user_email,))

        user= cursor_execucao.fetchone()
        database_connection.close()

        return user
    except Exception as e: 
        raise Exception(f"Database error: {str(e)}")

def buscar_user_por_userName(user_nameuser): 
    try: 
        database_connection= get_db_connection()
        cursor_execucao= database_connection.cursor()

        cursor_execucao.execute("SELECT id, name, email FROM users WHERE name = %s", (user_nameuser,))

        user= cursor_execucao.fetchone()
        database_connection.close()

        return user
    except Exception as e: 
        raise Exception(f"Database error: {str(e)}")