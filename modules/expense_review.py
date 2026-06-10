CATEGORY_LIMITS = {
    "Food": 5000,
    "Travel": 20000,
    "Shopping": 15000,
    "Bills": 30000,
    "Education": 50000,
    "Health": 50000,
    "Entertainment": 10000,
    "Other": 20000
}


def is_unusual_expense(category, amount):
    limit = CATEGORY_LIMITS.get(category, 20000)

    if amount > limit:
        return True, limit

    return False, limit