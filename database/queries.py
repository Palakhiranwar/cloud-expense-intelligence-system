from database.db_connection import get_connection

def add_expense(user_id, expense_date, category, amount, payment_mode, description):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO expenses 
    (user_id, expense_date, category, amount, payment_mode, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        expense_date,
        category,
        amount,
        payment_mode,
        description
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def get_all_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT id, expense_date, category, amount, payment_mode, description, created_at
    FROM expenses
    WHERE user_id = %s
    ORDER BY expense_date DESC
    """

    cursor.execute(query, (user_id,))

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses