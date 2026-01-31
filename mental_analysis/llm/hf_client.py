from gradio_client import Client

client = Client("Priyanshu292004/mental-health-insight-llm")

VIEW_MAP = {
    "daily": "Daily",
    "weekly": "Weekly",
    "yearly": "Yearly"
}

def get_llm_insight(
    test,
    view,
    trend,
    confidence,
    baseline_status,
    user_message=None,
    conversation_summary=None
):
    payload = {
        "test": test,
        "view": VIEW_MAP[view],
        "trend": trend,
        "confidence": confidence,
        "baseline_status": baseline_status
    }

    if user_message:
        payload["user_message"] = user_message

    if conversation_summary:
        payload["context"] = conversation_summary

    return client.predict(
        **payload,
        api_name="/generate_insight"
    )
