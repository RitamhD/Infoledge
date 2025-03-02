def activate_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ritam@9966',
        database='Infoledge' 
    )
    cursor = conn.cursor()
    return(conn, cursor);

def close_connection(conn, cursor):
    cursor.close()
    conn.close()
    return;
#-------------------------------------------------------------------------------------------------     

def show_tables():
    conn, cursor = activate_connection()
    cursor.execute("SHOW tables;")
    table = cursor.fetchall()
    close_connection(conn, cursor)
    return table


#   SHOW ALL CREDENTIALS RECORD:-
def show_credentials():
    conn, cursor = activate_connection()    
    cursor.execute("SELECT * FROM credentials")
    records = cursor.fetchall()
    close_connection(conn, cursor)
    return records


#   INSERT RECORD:-
def insert_into_credentials(user_name:str, user_email:str, user_password:str):
    try:
        conn, cursor = activate_connection()
        query = "INSERT INTO credentials (user_name, user_email, user_password) VALUES (%s, %s, %s)"  
        cursor.execute(query, (user_name, user_email, user_password))
        conn.commit()
        status = "***Successfully stored data***"
        close_connection(conn, cursor)
    except Exception as e:
        conn.rollback()
        status = f"There was an error...Try again\n{e}"
    finally:
        return status


#   DELETE RECORD
def delete_from_credentials(user_email: str):
    status = None
    try:
        conn, cursor = activate_connection()
        query_get_id = "SELECT user_id FROM credentials WHERE user_email=%s"
        cursor.execute(query_get_id, (user_email,))
        user_row = cursor.fetchone()
        
        if user_row is None:
            return "User not found !"
        
        # Delete the record:-
        query = "DELETE FROM credentials WHERE user_email=%s"
        cursor.execute(query, (user_email,))
        
        # Adjust the next userids:-
        user_id_to_delete = user_row[0]
        query = "UPDATE credentials SET user_id=(user_id-1) WHERE user_id > %s"
        cursor.execute(query, (user_id_to_delete,))
        
        # Adjust the Autoincrement:-    
        query = "SELECT MAX(user_id) FROM credentials"
        cursor.execute(query)
        max_user_id = cursor.fetchone()[0]
        
        if max_user_id is not None:
            query = "ALTER TABLE credentials AUTO_INCREMENT=%s"
            cursor.execute(query, (max_user_id+1,)) 
        else:
            query = "ALTER TABLE credentials AUTO_INCREMENT=1"
            cursor.execute(query)   
            
        conn.commit()        
        close_connection(conn, cursor)
        status = 'Successfully deleted'
    except Exception as e:
        conn.rollback()
        status = f"There was an error...Try again\n{e}"
    finally:
        return status


# print(insert_into_credentials('Anup', 'anup@gmail.com', 'anupranu'))
# print(delete_from_credentials('ritam@gmail.com'))
# print(show_credentials())