from database.queries import add_expense, get_all_expenses


add_expense("2026-05-31", "Food", 250.50, "UPI", "Lunch at canteen")

expenses = get_all_expenses()

for expense in expenses:
    print(expense)