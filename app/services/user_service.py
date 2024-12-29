from app.config import get_db_connection
import re

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
    
def validar_dados_user(name, email):
    
    #caracteres comuns em SQLinjection
    sql_injection_chars = re.compile(r"[;\'\"\-]{1,}", flags=re.UNICODE)

    # Validação do nome
    if not name or not isinstance(name, str) or len(name) < 3:
        return False, "Invalid name"
    if re.search(sql_injection_chars, name):
        return False, "Name contains invalid characters"
    
    # Validação do email 
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not email or not isinstance(email, str) or not re.match(email_regex, email):
        return False, "Invalid email format"
    
    return True, None

def verificar_user_exite(email):
    try: 
        database_connection = get_db_connection()
        cursor_execucao = database_connection.cursor()
        
        cursor_execucao.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor_execucao.fetchone()
        database_connection.close()

        return user is not None
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")

def adicionar_user_ao_db(name, email): 
    try: 
        database_connection = get_db_connection()
        cursor_execucao = database_connection.cursor()

        cursor_execucao.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))

        user_id = cursor_execucao.fetchone()[0]

        database_connection.commit()
        database_connection.close()

        return user_id
    except Exception as e: 
        raise Exception(f"Database error: {str(e)}")

    