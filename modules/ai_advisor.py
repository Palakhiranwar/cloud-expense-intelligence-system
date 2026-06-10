def generate_ai_response(df, question):

    question = question.lower()

    total = df["amount"].sum()

    category = (
        df.groupby("category")["amount"]
        .sum()
        .idxmax()
    )

    category_amount = (
        df.groupby("category")["amount"]
        .sum()
        .max()
    )

    monthly = (
        df.groupby(df["expense_date"].dt.to_period("M"))["amount"]
        .sum()
    )

    if "save" in question or "reduce" in question:
        return f"""
Based on your spending data:

Your highest spending category is {category}
with ₹{category_amount:.2f} spent.

Suggestions:
• Reduce unnecessary {category.lower()} expenses
• Set a monthly budget
• Review frequent small transactions

Your total recorded expense is ₹{total:.2f}.
"""

    elif "highest" in question or "spend" in question:
        return f"""
Your highest expense area is {category}
with ₹{category_amount:.2f}.

You should monitor this category closely.
"""

    elif "month" in question or "predict" in question:
        return f"""
Your monthly spending pattern:

{monthly.to_string()}

Try maintaining a consistent monthly budget.
"""

    else:
        return f"""
I analyzed your expenses.

Total spending: ₹{total:.2f}
Highest category: {category}

Ask me about:
• saving money
• spending patterns
• highest expenses
• monthly trends
"""