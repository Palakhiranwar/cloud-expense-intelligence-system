import pandas as pd


def create_expense_dataframe(expenses):

    if not expenses:
        return pd.DataFrame()

    df = pd.DataFrame(expenses)

    df["expense_date"] = pd.to_datetime(df["expense_date"])

    df["amount"] = df["amount"].astype(float)

    return df