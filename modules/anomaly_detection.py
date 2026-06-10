import pandas as pd


def detect_anomalies(df):

    if df.empty:
        return pd.DataFrame()

    anomaly_rows = []

    for category in df["category"].unique():

        category_df = df[df["category"] == category].copy()

        if len(category_df) < 3:
            continue

        average = category_df["amount"].mean()
        std_dev = category_df["amount"].std()

        if std_dev == 0:
            continue

        threshold = average + std_dev

        anomalies = category_df[
            category_df["amount"] > threshold
        ]

        anomaly_rows.append(anomalies)

    if anomaly_rows:
        return pd.concat(anomaly_rows).drop_duplicates()

    return pd.DataFrame()