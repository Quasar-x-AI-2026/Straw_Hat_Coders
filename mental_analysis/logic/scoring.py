def score_phq9(responses):
    total = sum(responses)
    if total <= 4:
        severity = "Minimal"
    elif total <= 9:
        severity = "Mild"
    elif total <= 14:
        severity = "Moderate"
    elif total <= 19:
        severity = "Moderately Severe"
    else:
        severity = "Severe"
    return total, severity


def score_gad7(responses):
    total = sum(responses)
    if total <= 4:
        severity = "Minimal"
    elif total <= 9:
        severity = "Mild"
    elif total <= 14:
        severity = "Moderate"
    else:
        severity = "Severe"
    return total, severity


def score_who5(responses):
    raw = sum(responses)
    percentage = raw * 4
    return raw, percentage

def score_dass21(responses, questions):
    scores = {
        "Depression": 0,
        "Anxiety": 0,
        "Stress": 0
    }

    for response, q in zip(responses, questions):
        scores[q["subscale"]] += response

    # DASS-21 standard: multiply by 2
    for key in scores:
        scores[key] *= 2

    return scores
