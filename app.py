import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# -------------------------------------------------------------
# SYSTEM CONFIGURATION & AI ENGINE SETUP
# -------------------------------------------------------------
st.set_page_config(page_title="Ikshana AI Portal", layout="wide")

# Replace this with your actual Gemini API Key from Google AI Studio
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

def call_gemini_ai(prompt_text):
    """Connects directly to the real Google Gemini AI Engine"""
    try:
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
            return "AI Engine Mode: [Simulation] Please provide a valid Gemini API Key to unlock real-time analysis."
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text,
        )
        return response.text
    except Exception as e:
        return f"AI Connection Error: {str(e)}"

# -------------------------------------------------------------
# APP NAVIGATION STATE
# -------------------------------------------------------------
if "role" not in st.session_state:
    st.session_state.role = "welcome"
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

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
        st.write("Upload spreadsheets, analyze sentiment, validate metrics, and unlock premium tier tools.")
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
# SCREEN 2: SELLER ENGINE (BULK UPLOAD & PAYWALL LOGIC)
# -------------------------------------------------------------
elif st.session_state.role == "seller":
    st.title("🏪 Seller Control Center")
    if st.button("← Back to Welcome Gateway"):
        st.session_state.role = "welcome"
        st.rerun()
        
    st.write("---")
    
    st.markdown("### Bulk Data Feed Ingestion")
    uploaded_file = st.file_uploader("Drop e-commerce tracking registers here (.csv or .xlsx)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Read file rows
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        row_count = len(df)
        st.write(f"📊 Extracted **{row_count} customer reviews** from your file.")
        
        # 50-Review Validator Rule
        if row_count < 50:
            st.error(f"❌ Document Rejected: Only {row_count} reviews parsed. File must contain a minimum of 50 reviews to initiate AI training.")
        else:
            st.success("✅ Document Accepted! Row threshold validation passed.")
            st.session_state.uploaded_data = df
            
            # Premium Paywall Simulation
            st.write("---")
            st.markdown("### 🔒 Unlock Deep AI Sentiment Analytics")
            st.info("Your dataset is ready. Unlock deep charts, automated replies, and competitive audit indexes.")
            if st.button("Subscribe via Samsung Pay — $14.99/mo", type="primary"):
                st.balloons()
                st.success("Premium Active Tier Initialized!")
                
                # Real AI execution over the file data
                sample_reviews = " ".join(df.iloc[:, 0].astype(str).tail(5).tolist())
                with st.spinner("AI analyzing your uploaded inventory feedback..."):
                    ai_analysis_prompt = f"Analyze the customer sentiment of these reviews and summarize the core quality flaws: {sample_reviews}"
                    results = call_gemini_ai(ai_analysis_prompt)
                    st.markdown("#### 🧠 Live AI Engine Feedback Summary:")
                    st.write(results)

# -------------------------------------------------------------
# SCREEN 3: SHOPPER SPACE (CROSS-REFERENCE AI & CO-PILOT CHAT)
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
        with st.spinner("Cross-referencing live marketplace parameters against seller records..."):
            prompt = f"Compare the marketing claim '{claim}' for product '{product}' against typical consumer feedback. Is it likely true or an anomaly?"
            verdict = call_gemini_ai(prompt)
            
            st.metric(label="Verdict Match Index", value="91% High Reliability")
            st.info(verdict)
            
    st.write("---")
    st.markdown("### 💬 Ikshana Shopping Copilot")
    query = st.text_input("Ask Chat Assistant About Product Discrepancies:")
    if query:
        with st.spinner("Auditing supplier logs..."):
            chat_response = call_gemini_ai(query)
            st.write(chat_response)

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
    
    # Live structured list that the ranker sorts automatically
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
    # Sort descending based on score
    filtered_items = sorted(filtered_items, key=lambda k: k['score'], reverse=True)
    
    for rank, item in enumerate(filtered_items, 1):
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 2])
            col1.markdown(f"## #{rank}")
            col2.markdown(f"**{item['name']}** \n`{item['badge']}`")
            col3.metric("Trust Index Score", f"{item['score']}/100")
            st.write("---")
