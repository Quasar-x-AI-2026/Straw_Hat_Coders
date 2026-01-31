import streamlit as st

def render_screener(tool):
    st.subheader(tool["tool"])
    responses = []

    progress = st.progress(0)

    for i, question in enumerate(tool["questions"]):
        progress.progress((i + 1) / len(tool["questions"]))

        answer = st.radio(
            question,
            tool["scale"],
            format_func=lambda x: tool["labels"][x],
            key=f"{tool['tool']}_{i}"
        )
        responses.append(answer)

    return responses

def render_dass21(tool):
    import streamlit as st

    st.subheader(tool["tool"])
    responses = []

    progress = st.progress(0)

    for i, q in enumerate(tool["questions"]):
        progress.progress((i + 1) / len(tool["questions"]))

        answer = st.radio(
            q["text"],
            tool["scale"],
            format_func=lambda x: tool["labels"][x],
            key=f"DASS21_{i}"
        )
        responses.append(answer)

    return responses
