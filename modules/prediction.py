import pandas as pd


def predict_future_expense(df):

    if df.empty:
        return 0

    monthly_expense = (
        df.groupby(df["expense_date"].dt.to_period("M"))["amount"]
        .sum()
    )

    if len(monthly_expense) == 1:
        return monthly_expense.iloc[0]

    prediction = monthly_expense.tail(3).mean()

    return round(prediction, 2)