def generate_insights(df):

    insights = []

    if df.empty:
        return insights

    total_expense = df["amount"].sum()

    top_category = (
        df.groupby("category")["amount"]
        .sum()
        .idxmax()
    )

    top_category_amount = (
        df.groupby("category")["amount"]
        .sum()
        .max()
    )

    category_percentage = (
        (top_category_amount / total_expense) * 100
    )

    insights.append(
        f"Highest spending category is {top_category}, contributing {category_percentage:.1f}% of total expenses."
    )

    average_expense = df["amount"].mean()

    if average_expense > 5000:
        insights.append(
            "Your average expense value is relatively high. Consider monitoring discretionary spending."
        )

    if len(df[df["payment_mode"] == "Credit Card"]) > len(df) * 0.5:
        insights.append(
            "Most expenses are made using Credit Card. Ensure repayment tracking to avoid debt accumulation."
        )

    if total_expense > 50000:
        insights.append(
            "Overall spending is significantly high. Budget optimization may help reduce monthly outflow."
        )

    return insights