def calculate_trend(df):
    if len(df) < 2:
        return "Insufficient Data"

    delta = df["score"].iloc[-1] - df["score"].iloc[0]

    if delta > 1:
        return "Increasing"
    if delta < -1:
        return "Decreasing"
    return "Stable"
