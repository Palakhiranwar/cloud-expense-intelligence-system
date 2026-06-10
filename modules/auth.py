from database.db_connection import get_connection
import hashlib


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()



def signup(name, email, password):

    connection = get_connection()
    cursor = connection.cursor()


    try:

        check_query = """
        SELECT email
        FROM users
        WHERE email = %s
        """


        cursor.execute(
            check_query,
            (email,)
        )


        result = cursor.fetchone()


        if result:

            return False



        hashed = hash_password(password)


        insert_query = """
        INSERT INTO users
        (name,email,password)
        VALUES (%s,%s,%s)
        """


        cursor.execute(
            insert_query,
            (
                name,
                email,
                hashed
            )
        )


        connection.commit()


        return True



    finally:

        cursor.close()
        connection.close()




def login(email,password):

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)


    hashed = hash_password(password)


    query = """
    SELECT *
    FROM users
    WHERE email=%s
    AND password=%s
    """


    cursor.execute(
        query,
        (
            email,
            hashed
        )
    )


    user = cursor.fetchone()


    cursor.close()
    connection.close()


    return user