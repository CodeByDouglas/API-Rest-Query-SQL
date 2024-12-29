from app.config import get_db_connection

def limpar_email_de_teste(email):
   
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        connection.commit()
        connection.close()
    except Exception as e:
        raise Exception(f"Erro ao limpar email de teste: {str(e)}")
