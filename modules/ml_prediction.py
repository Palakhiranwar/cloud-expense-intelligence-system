import pandas as pd

from sklearn.ensemble import RandomForestRegressor


def predict_ml_expense(df):

    if df.empty:
        return None


    if len(df) < 3:
        return None


    monthly = (
        df.groupby(df["expense_date"].dt.to_period("M"))
        .agg(
            amount=("amount", "sum"),
            transactions=("amount", "count")
        )
        .reset_index()
    )


    monthly["average_transaction"] = (
        monthly["amount"] /
        monthly["transactions"]
    )


    monthly["previous_month"] = (
        monthly["amount"].shift(1)
    )


    monthly["rolling_average"] = (
        monthly["amount"]
        .rolling(
            window=2,
            min_periods=1
        )
        .mean()
    )


    monthly = monthly.dropna()


    if len(monthly) < 2:
        return None


    X = monthly[
        [
            "previous_month",
            "transactions",
            "average_transaction",
            "rolling_average"
        ]
    ]


    y = monthly["amount"]


    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )


    model.fit(
        X,
        y
    )


    next_data = pd.DataFrame(
        [
            {
                "previous_month": monthly["amount"].iloc[-1],
                "transactions": monthly["transactions"].mean(),
                "average_transaction": monthly["average_transaction"].mean(),
                "rolling_average": monthly["rolling_average"].iloc[-1]
            }
        ]
    )


    prediction = model.predict(next_data)


    return round(
        float(prediction[0]),
        2
    )