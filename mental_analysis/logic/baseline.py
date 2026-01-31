def calculate_baseline(df, min_points=5):
    """
    Calculates personal baseline using first few stable points.
    Returns None if insufficient data.
    """

    if df is None or len(df) < min_points:
        return None

    baseline_value = df["score"].iloc[:min_points].mean()
    return round(baseline_value, 2)
