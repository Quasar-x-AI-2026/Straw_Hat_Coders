from mental_analysis.llm.prompt_builder import SYSTEM_PROMPT, build_user_prompt

# Placeholder for Hugging Face / API later
def generate_insight(context: dict):
    user_prompt = build_user_prompt(context)

    # ⚠️ Replace this later with HuggingFace / API call
    response = f"""
Trend Summary:
The data shows a {context['trend'].lower()} pattern over the selected period.

Confidence:
This interpretation is based on {context['confidence'].lower()} confidence data.

Reflection Questions:
- What factors may have influenced this pattern?
- Did anything change in your routine during this period?
"""

    return response.strip()
