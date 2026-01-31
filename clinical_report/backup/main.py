import streamlit as st
import pandas as pd
import plotly.express as px
from processor import analyze_medical_report, get_ai_insights
from database import init_db, save_report_data, get_trend_data, get_connection

# Page Config
st.set_page_config(page_title="Smart Health Analytics", layout="wide")
st.title("🏥 AI Clinical Record System")

# Initialize DB on load
init_db()

# --- TABS LAYOUT ---
tab1, tab2, tab3 = st.tabs(["📂 Upload Report", "📈 Health Trends", "🤖 AI Insights"])

# ==========================================
# TAB 1: UPLOAD & PROCESS
# ==========================================
with tab1:
    st.header("Upload Medical Record")
    uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display Image
        st.image(uploaded_file, caption="Uploaded Report", width=300)
        
        if st.button("🔍 Extract Data"):
            with st.spinner("AI is reading the report..."):
                # Convert file to bytes for Gemini
                image_bytes = uploaded_file.getvalue()
                
                # Call Processor
                extracted_data = analyze_medical_report(image_bytes)
                
                if extracted_data:
                    st.success("Data Extracted Successfully!")
                    
                    # Store in Session State (Temporary) to review before saving
                    st.session_state['current_data'] = extracted_data
                else:
                    st.error("Failed to extract data. Please try again.")

    # Review & Save Section
    if 'current_data' in st.session_state:
        data = st.session_state['current_data']
        
        st.subheader("📝 Review Extracted Data")
        
        # Show Metadata
        col1, col2 = st.columns(2)
        col1.info(f"**Patient:** {data['metadata'].get('patient_name')}")
        col2.info(f"**Date:** {data['metadata'].get('report_date')}")
        
        # Show Results in Table
        df_results = pd.DataFrame(data['results'])
        st.dataframe(df_results)
        
        if st.button("💾 Save to Database"):
            success, msg = save_report_data(data['metadata'], data['results'])
            if success:
                st.success(f"Saved! {msg}")
                del st.session_state['current_data'] # Clear after save
            else:
                st.error(f"Error saving: {msg}")

# ==========================================
# TAB 2: TRENDS & GRAPHS
# ==========================================
with tab2:
    st.header("Health Trends Analysis")
    
    # User selects a parameter to view
    # (Real app mein ye list DB se dynamic honi chahiye, abhi hardcode example hai)
    parameter = st.text_input("Enter Test Name to Track (e.g., Hemoglobin, Glucose):", "Hemoglobin")
    
    if st.button("Show Trend"):
        df_trend = get_trend_data(parameter)
        
        if not df_trend.empty:
            st.write(f"Showing trends for: **{parameter}**")
            
            # Line Chart
            fig = px.line(df_trend, x='report_date', y='value_numeric', 
                          markers=True, title=f"{parameter} Over Time",
                          labels={'value_numeric': f'Value ({df_trend.iloc[0]["unit"]})'})
            
            # Highlight abnormal zones (Simple visual cue)
            fig.update_traces(line_color='#1f77b4', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df_trend)
        else:
            st.warning("No data found for this parameter yet.")

# ==========================================
# TAB 3: AI INSIGHTS
# ==========================================
with tab3:
    st.header("Ask AI about your Health")
    
    conn = get_connection()
    # Pura data fetch karte hain context ke liye
    full_history_df = pd.read_sql("SELECT * FROM test_results", conn)
    conn.close()
    
    if not full_history_df.empty:
        # Convert DB data to text summary for AI
        history_text = full_history_df.to_string()
        
        user_question = st.text_input("Ask a question (e.g., 'Is my sugar level increasing?', 'Any critical flags?')")
        
        if user_question and st.button("Get Answer"):
            with st.spinner("Analyzing records..."):
                answer = get_ai_insights(history_text, user_question)
                st.markdown(f"### 💡 AI Response:\n{answer}")
    else:
        st.info("Upload some reports first to get insights.")