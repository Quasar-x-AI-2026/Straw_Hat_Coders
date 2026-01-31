def interpretation_text(trend, confidence, view):
    scopes = {
        "daily": "short-term daily pattern",
        "weekly": "weekly pattern",
        "yearly": "long-term pattern"
    }

    scope = scopes[view]

    if trend == "Insufficient Data":
        return f"Not enough data to understand the {scope}."

    if confidence == "Low":
        return f"A possible {trend.lower()} {scope} is observed, based on limited data."

    return f"A clear {trend.lower()} {scope} is observed."
