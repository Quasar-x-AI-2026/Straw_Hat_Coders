def build_flan_prompt(context, chat_history, user_message=None):
    system_rules = """
You are a mental health insight assistant.
Do NOT diagnose or prescribe medication.
Encourage reflection using supportive language.
"""

    analysis = f"""
Assessment: {context['test']}
Timeframe: {context['view']}
Trend: {context['trend']}
Confidence: {context['confidence']}
Baseline: {context['baseline_status']}
"""

    history = ""
    for msg in chat_history[-4:]:
        history += f"{msg['role'].capitalize()}: {msg['content']}\n"

    if user_message:
        user = f"User: {user_message}"
    else:
        user = "Explain the insight clearly."

    return f"""
{system_rules}

{analysis}

Conversation so far:
{history}

{user}

Assistant:
"""
