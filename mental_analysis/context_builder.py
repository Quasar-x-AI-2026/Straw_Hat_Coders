def build_insight_context(
    test,
    view,
    trend,
    confidence,
    baseline_status,
    reflection
):
    return {
        "test": test,
        "view": view,
        "trend": trend,
        "confidence": confidence,
        "baseline_status": baseline_status,
        "reflection": reflection
    }
