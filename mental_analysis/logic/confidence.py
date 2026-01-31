def calculate_confidence(df, view):
    n = len(df)

    if view == "daily":
        if n < 3:
            return "low"
        elif n < 7:
            return "medium"
        else:
            return "high"

    if view == "weekly":
        if n < 2:
            return "low"
        elif n < 4:
            return "medium"
        else:
            return "high"

    if view == "yearly":
        if n < 2:
            return "low"
        else:
            return "medium"
