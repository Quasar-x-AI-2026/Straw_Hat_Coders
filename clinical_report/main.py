import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from processor import analyze_medical_report, get_chat_response, generate_trend_analysis
from database import init_db, save_report_data, get_trend_data, get_connection, get_unique_test_names

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="Smart Health AI", layout="wide", page_icon="🏥")

# Custom CSS for Professional UI & Full Width Chat
st.markdown("""
<style>
    /* Main Header Styling */
    .main-header {font-size: 2.5rem; color: #4F8BF9; font-weight: 700; margin-bottom: 10px;}
    
    /* Upload Section Card */
    .upload-card {padding: 20px; background-color: #f8f9fa; border-radius: 10px; border: 1px solid #ddd;}
    
    /* CHAT INPUT FIX: Stretch to Whole Screen Width */
    .stChatInput {
        position: fixed; 
        bottom: 0; 
        left: 0;
        right: 0;
        width: 100%;
        padding: 20px; 
        z-index: 100; 
        background-color: white;
        border-top: 1px solid #ddd;
    }
    
    /* Input field centering */
    .stChatInputContainer {
        max-width: 1200px; 
        margin: auto;
    }
    
    /* Padding to prevent content hiding behind chat bar */
    .main .block-container {padding-bottom: 150px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏥 AI Clinical Record System</div>', unsafe_allow_html=True)

# Initialize Database & Session State
init_db()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def parse_range(range_str):
    if not range_str or not isinstance(range_str, str) or range_str.lower() == 'unknown':
        return None, None
    try:
        clean_str = range_str.lower()
        for word in ['reference', 'range', 'normal', 'values', ':', '(', ')']:
            clean_str = clean_str.replace(word, '')
        clean_str = clean_str.replace('to', '-').strip()
        parts = clean_str.split('-')
        if len(parts) == 2:
            return float(parts[0].strip()), float(parts[1].strip())
    except:
        pass
    return None, None

# ==========================================
# 3. TABS LAYOUT
# ==========================================
tab1, tab2, tab3 = st.tabs(["📂 Upload & Verify", "📈 Trends & Insights", "💬 AI Doctor Chat"])

# --------------------------------------------------------------------------------
# TAB 1: PROFESSIONAL UPLOAD UI
# --------------------------------------------------------------------------------
with tab1:
    col_left, col_right = st.columns([1, 1.5], gap="large")
    
    with col_left:
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.subheader("📤 Step 1: Upload Report")
        st.info("Supported formats: JPG, PNG, JPEG")
        
        uploaded_file = st.file_uploader("Choose file", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file:
            st.success("✅ Image Loaded")
            st.image(uploaded_file, caption="Preview", use_container_width=True)
            
            if st.button("🔍 Extract Data Now", type="primary", use_container_width=True):
                with st.spinner("AI is analyzing report..."):
                    image_bytes = uploaded_file.getvalue()
                    extracted_data = analyze_medical_report(image_bytes)
                    if extracted_data:
                        st.session_state['current_data'] = extracted_data
                        st.rerun()
                    else:
                        st.error("Extraction failed. Try a clearer image.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if 'current_data' in st.session_state:
            st.subheader("📝 Step 2: Verify & Edit")
            data = st.session_state['current_data']
            meta = data.get('metadata', {})
            
            # Metadata Display
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**👤 Patient:** {meta.get('patient_name', 'Unknown')}")
            c2.markdown(f"**📅 Date:** {meta.get('report_date', 'Unknown')}")
            c3.markdown(f"**🏥 Lab:** {meta.get('lab_name', 'Unknown')}")
            
            # Editable Table
            if 'results' in data:
                df_preview = pd.DataFrame(data['results'])
                st.markdown("check the values below. **Double click cells to edit** if AI made a mistake.")
                edited_df = st.data_editor(df_preview, num_rows="dynamic", use_container_width=True)
                
                # Save Buttons
                col_b1, col_b2 = st.columns([1, 1])
                if col_b1.button("💾 CONFIRM & SAVE", type="primary", use_container_width=True):
                    updated_results = edited_df.to_dict('records')
                    success, msg = save_report_data(data['metadata'], updated_results)
                    if success:
                        st.balloons()
                        st.toast("Record Saved to Database!", icon="✅")
                        del st.session_state['current_data']
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")
                
                if col_b2.button("❌ Cancel", type="secondary", use_container_width=True):
                    del st.session_state['current_data']
                    st.rerun()
        else:
            # Empty State
            st.info("👈 Please upload a report from the left side to see data here.")

# --------------------------------------------------------------------------------
# TAB 2: TRENDS & AI INSIGHTS (UPDATED WITH DUAL GRAPHS)
# --------------------------------------------------------------------------------
with tab2:
    st.subheader("📈 Health Dashboard")
    
    available_tests = get_unique_test_names()
    available_tests.sort()
    
    if available_tests:
        col_sel, _ = st.columns([1, 2])
        with col_sel:
            selected_test = st.selectbox("📊 Select Test Parameter:", available_tests)
        
        if selected_test:
            df_trend = get_trend_data(selected_test)
            
            if not df_trend.empty:
                # Process Dates
                df_trend['report_date'] = pd.to_datetime(df_trend['report_date'], errors='coerce')
                df_trend = df_trend.dropna(subset=['report_date'])
                df_trend = df_trend.sort_values('report_date')
                
                if not df_trend.empty:
                    
                    # --- GRAPH 1: TREND LINE + GREEN BAND ---
                    st.markdown("### 🔹 Trend Analysis")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.set_facecolor('white')
                    ax.grid(color='#f0f0f0', linestyle='--', linewidth=1)
                    
                    dates = df_trend['report_date']
                    values = df_trend['value_numeric']
                    latest_range = df_trend.iloc[-1]['reference_range']
                    low, high = parse_range(latest_range)
                    
                    # 1. Green Band (Normal Zone)
                    if low is not None and high is not None:
                        ax.fill_between(dates, low, high, color='#28a745', alpha=0.1, label=f'Normal ({low}-{high})')
                        colors = ['#dc3545' if (v < low or v > high) else '#28a745' for v in values]
                    else:
                        colors = '#007bff'
                    
                    # Line & Points
                    ax.plot(dates, values, color='#333', linewidth=2, label='Trend')
                    ax.scatter(dates, values, color=colors, s=100, zorder=5, edgecolors='white', linewidth=2)
                    
                    # Labels on points
                    for i, txt in enumerate(values):
                        ax.annotate(f"{txt}", (dates.iloc[i], values.iloc[i]), xytext=(0,12), textcoords="offset points", ha='center', fontsize=9, fontweight='bold')
                        
                    ax.set_ylabel(df_trend.iloc[0]['unit'])
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
                    fig.autofmt_xdate()
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.legend(frameon=False)
                    
                    st.pyplot(fig)

                    # --- GRAPH 2: DATA COMPARISON (BAR CHART) ---
                    st.markdown("### 🔹 Data Comparison")
                    fig2, ax2 = plt.subplots(figsize=(10, 3))
                    
                    # Convert dates to string for distinct bars
                    date_labels = df_trend['report_date'].dt.strftime('%d %b %Y')
                    
                    # Create Bars
                    bars = ax2.bar(date_labels, values, color='#4F8BF9', alpha=0.7, width=0.4)
                    
                    # Add values on top of bars
                    ax2.bar_label(bars, fmt='%.1f')
                    
                    # Styling
                    ax2.set_ylabel("Value")
                    ax2.spines['top'].set_visible(False)
                    ax2.spines['right'].set_visible(False)
                    ax2.grid(axis='y', linestyle='--', alpha=0.5)
                    
                    st.pyplot(fig2)
                    
                    # --- AI ANALYSIS SECTION ---
                    st.divider()
                    st.subheader(f"🤖 AI Analysis: {selected_test}")
                    
                    if st.button("✨ Generate AI Insights & Recommendations", type="primary"):
                        with st.spinner("Analyzing your health trends..."):
                            range_info = f"(Normal Range: {latest_range})" if latest_range else ""
                            summary = df_trend[['report_date', 'value_numeric']].to_string()
                            prompt_data = f"Test: {selected_test} {range_info}\nData:\n{summary}"
                            
                            advice = generate_trend_analysis(selected_test, prompt_data)
                            st.markdown(advice)
                else:
                    st.warning("Invalid dates found in records.")
            else:
                st.warning("No data found for this test.")
    else:
        st.info("📭 No records found. Upload a report in Tab 1 first.")

# --------------------------------------------------------------------------------
# TAB 3: CHATBOT (FULL WIDTH FIXED BOTTOM)
# --------------------------------------------------------------------------------
with tab3:
    st.markdown("### 💬 Chat with Dr. AI")
    
    # 1. Load History
    conn = get_connection()
    history = pd.read_sql("SELECT * FROM test_results", conn).to_string()
    conn.close()

    # 2. Display Messages (Container allows scrolling)
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Spacer div to push last message above the input box
        st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

    # 3. Input Box (Automatically fixed at bottom by CSS above)
    if query := st.chat_input("Type your health question here..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = get_chat_response(history, st.session_state.messages, query)
                st.markdown(ans)
        
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()