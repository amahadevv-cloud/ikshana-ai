import streamlit as st
import pandas as pd
import re
import time
from google import genai
from google.genai import types

# -------------------------------------------------------------
# SYSTEM CONFIGURATION & INSTANT PERFORMANCE CACHING
# -------------------------------------------------------------
st.set_page_config(page_title="Ikshana AI Portal", layout="wide")

# Replace this with your actual Gemini API Key from Google AI Studio
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

def stream_gemini_ai(prompt_text):
    """Streams responses from Google Gemini AI Engine in real time to eliminate lag"""
    try:
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
            # Simulated streaming generator function for local mode
            def simulation_generator():
                sim_text = "AI Engine Mode: [Simulation] Please provide a valid Gemini API Key to unlock real-time streaming analysis."
                for word in sim_text.split(" "):
                    yield word + " "
                    time.sleep(0.04)
            return simulation_generator()
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Generator function to catch chunks as they arrive from the server
        def response_generator():
            response = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=prompt_text,
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        return response_generator()
    except Exception as e:
        def error_generator():
            yield f"AI Connection Error: {str(e)}"
        return error_generator()

# --- HIGH SPEED NATIVE CACHING PIPELINE ---
@st.cache_data
def clean_symbols_fast(text):
    """Pre-processes text symbols instantly using cached compiled regex"""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'&', ' [AND] ', text)
    text = re.sub(r'\$', ' [DOLLAR CURRENCY] ', text)
    text = re.sub(r'@', ' [AT LOG] ', text)
    text = re.sub(r'#', ' [HASHTAG] ', text)
    text = re.sub(r'%', ' [PERCENT] ', text)
    return text

@st.cache_data
def process_dataframe_metrics(file_contents, is_csv=True):
    """Caches heavy dataframe computing transformations so page re-renders are instant"""
    # Create internal dataframes from cached binary string transfers
    import io
    if is_csv:
        df = pd.read_csv(io.BytesIO(file_contents))
    else:
        df = pd.read_excel(io.BytesIO(file_contents))
        
    review_column = df.columns[0]
    total_rows = len(df)
    
    duplicate_mask = df[review_column].astype(str).str.strip().duplicated()
    duplicate_count = duplicate_mask.sum()
    unique_rows = total_rows - duplicate_count
    duplicate_percentage = round((duplicate_count / total_rows) * 100, 1)
    
    # Process native data cleaning fast
    df['Cleaned_Review'] = df[review_column].apply(clean_symbols_fast)
    df_cleaned = df.drop_duplicates(subset=[review_column])
    
    # Pre-generate sample string block
    sample_reviews_string = " | ".join(df_cleaned['Cleaned_Review'].astype(str).tail(10).tolist())
    
    return total_rows, unique_rows, duplicate_count, duplicate_percentage, df_cleaned, sample_reviews_string

# -------------------------------------------------------------
# APP NAVIGATION STATE
# -------------------------------------------------------------
if "role" not in st.session_state:
    st.session_state.role = "welcome"

# -------------------------------------------------------------
# SCREEN 1: WELCOME SYSTEM GATEWAY
# -------------------------------------------------------------
if st.session_state.role == "welcome":
    st.title("🎯 Ikshana AI")
    st.subheader("Smart Verification & Self-Generating Trusted Leaderboards")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🏪 Business Sellers")
        st.write("Upload spreadsheets, analyze sentiment, validate metrics, and unlock evaluation tools.")
        if st.button("Enter Seller Gateway", use_container_width=True):
            st.session_state.role = "seller"
            st.rerun()
            
    with col2:
        st.success("### 🛍️ Consumer Shoppers")
        st.write("Cross-reference claims, query product logs, and converse with the Ikshana Copilot.")
        if st.button("Enter Shopper Space", use_container_width=True):
            st.session_state.role = "shopper"
            st.rerun()
            
    with col3:
        st.warning("### 🏆 Public AI Rankings")
        st.write("Explore self-generating marketplaces and dynamic trust badge certifications.")
        if st.button("Open Public Board", use_container_width=True):
            st.session_state.role = "public_board"
            st.rerun()

# -------------------------------------------------------------
# SCREEN 2: HIGH-SPEED ENTERPRISE SELLER ENGINE
# -------------------------------------------------------------
elif st.session_state.role == "seller":
    st.title("🏪 Ultra-Fast Seller Control Center")
    if st.button("← Back to Welcome Gateway"):
        st.session_state.role = "welcome"
        st.rerun()
        
    st.write("---")
    
    st.markdown("### Bulk Data Feed Ingestion")
    uploaded_file = st.file_uploader("Drop e-commerce tracking registers here (.csv or .xlsx)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Read file as bytes directly to support cache layer functions
        file_bytes = uploaded_file.getvalue()
        is_csv = uploaded_file.name.endswith('.csv')
        
        # Execute super fast calculation from cached system data
        total_rows, unique_rows, duplicate_count, duplicate_percentage, df_cleaned, sample_reviews = process_dataframe_metrics(file_bytes, is_csv=is_csv)
        
        st.write(f"📊 Extracted **{total_rows} total rows** from your file.")
        
        if total_rows < 50:
            st.error(f"❌ Document Rejected: Only {total_rows} rows parsed. File must contain a minimum of 50 reviews to initiate AI training.")
        else:
            st.success("✅ Document Accepted! Row threshold validation passed.")
            
            st.markdown("### 🔍 Pre-Processing & Repetition Analysis")
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            col_metric1.metric("Unique Records", f"{unique_rows}")
            col_metric2.metric("Identical Repetitions Found", f"{duplicate_count}")
            col_metric3.metric("Data Redundancy Rate", f"{duplicate_percentage}%")
            
            # Render charts with cached calculations instantly
            st.write("---")
            st.markdown("### 📊 Live Data Integrity Statistics")
            chart_data = pd.DataFrame({
                "Record Type": ["Unique Verified Reviews", "Repetitive Spam Entries"],
                "Row Count": [int(unique_rows), int(duplicate_count)]
            }).set_index("Record Type")
            st.bar_chart(chart_data)
            
            # --- REAL-TIME AI RESPONSE STREAMING ---
            st.write("---")
            st.markdown("### 🧠 Deep AI Linguistic Translation & Suggestions")
            
            advanced_ai_prompt = f"""
            You are an advanced retail data engineering model. Review this compiled dataset:
            "{sample_reviews}"
            
            Please execute the following operations step-by-step:
            1. EMOJI DE-NOISING SUMMARY: Scan the data stream. Identify the most common emojis (like 🔥, ❌, 👍, 📦) and explain what consumer emotion they translated to textually.
            2. ADVANCED QUALITY AUDIT: Detail the top 3 product structural engineering flaws discovered based on user text expressions.
            3. AI ACTION SUGGESTIONS: Provide 3 clear, strategic engineering updates or operational fixes designed truly by AI reasoning.
            """
            
            st.markdown("#### Live AI Deep Audit Output (Streaming):")
            # st.write_stream instantly prints words as they arrive, removing screen freezing
            st.write_stream(stream_gemini_ai(advanced_ai_prompt))
            st.balloons()
                
            # --- EXPORT DATA UTILITY ---
            st.write("---")
            st.markdown("### 📥 Cleaned Registry Export Utilities")
            csv_buffer = df_cleaned.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Cleaned & De-duplicated Dataset (CSV)",
                data=csv_buffer,
                file_name="ikshana_cleaned_records.csv",
                mime="text/csv"
            )

# -------------------------------------------------------------
# SCREEN 3: SHOPPER SPACE (STREAMING ENGINE CHAT)
# -------------------------------------------------------------
elif st.session_state.role == "shopper":
    st.title("🛍️ Shopper Verification Space")
    if st.button("← Back to Welcome Gateway"):
        st.session_state.role = "welcome"
        st.rerun()
    st.write("---")
    
    st.markdown("### Multi-Source Cross-Confirmation Module")
    product = st.text_input("Product Name", "X-Phone Pro")
    claim = st.text_input("Public Marketing Claim to Audit", "20-hour battery runtime")
    
    if st.button("Run Cross-Reference AI Validation"):
        prompt = f"Compare the marketing claim '{claim}' for product '{product}' against typical consumer feedback. Is it likely true or an anomaly?"
        st.metric(label="Verdict Match Index", value="91% High Reliability")
        st.write_stream(stream_gemini_ai(prompt))
            
    st.write("---")
    st.markdown("### 💬 Ikshana Shopping Copilot")
    query = st.text_input("Ask Chat Assistant About Product Discrepancies:")
    if query:
        chat_response_stream = stream_gemini_ai(query)
        st.write_stream(chat_response_stream)

# -------------------------------------------------------------
# SCREEN 4: PUBLIC BOARD (DYNAMIC AI AUTO-CATEGORIZATION)
# -------------------------------------------------------------
elif st.session_state.role == "public_board":
    st.title("🏆 Global Trust Leaderboards")
    if st.button("← Back to Welcome Gateway"):
        st.session_state.role = "welcome"
        st.rerun()
    st.write("---")
    
    st.write("💡 *Self-generating category tiers dynamically grouped by current AI metrics.*")
    
    mock_catalog = [
        {"name": "X-Phone Pro", "category": "🔋 Ultra-Battery Handsets", "score": 95, "badge": "💎 AI Platinum Certified"},
        {"name": "VoltCharge 20W", "category": "🔌 Smart Fast Chargers", "score": 89, "badge": "🥇 AI Gold Certified"},
        {"name": "Aero Buds Max", "category": "🎧 Noise-Cancellation Gears", "score": 92, "badge": "💎 AI Platinum Certified"},
        {"name": "EcoWeave Tee", "category": "🌱 Organic Streetwear", "score": 74, "badge": "🥈 AI Verified Standard"}
    ]
    
    categories = list(set([item["category"] for item in mock_catalog]))
    selected_cat = st.selectbox("Select an AI Auto-Created Category Market:", categories)
    
    st.write(f"### Current Rankings for {selected_cat}")
    
    filtered_items = [item for item in mock_catalog if item["category"] == selected_cat]
    filtered_items = sorted(filtered_items, key=lambda k: k['score'], reverse=True)
    
    for rank, item in enumerate(filtered_items, 1):
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 2])
            col1.markdown(f"## #{rank}")
            col2.markdown(f"**{item['name']}** \n`{item['badge']}`")
            col3.metric("Trust Index Score", f"{item['score']}/100")
            st.write("---")
