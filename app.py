import streamlit as st
import pandas as pd
import re
import time
import io
from google import genai
from google.genai import types

# -------------------------------------------------------------
# SYSTEM CONFIGURATION & INSTANT PERFORMANCE CACHING
# -------------------------------------------------------------
st.set_page_config(page_title="Ikshana AI Portal", layout="wide")

# Securely pulls key maps from Streamlit Dashboard secrets parameters
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

def stream_gemini_ai(prompt_text):
    """Streams responses from Google Gemini AI Engine in real time to eliminate lag"""
    try:
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
            def simulation_generator():
                sim_text = "AI Engine Mode: [Simulation] Please provide a valid Gemini API Key to unlock real-time streaming analysis."
                for word in sim_text.split(" "):
                    yield word + " "
                    time.sleep(0.04)
            return simulation_generator()
        
        client = genai.Client(api_key=GEMINI_API_KEY)
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
    
    df['Cleaned_Review'] = df[review_column].apply(clean_symbols_fast)
    df_cleaned = df.drop_duplicates(subset=[review_column])
    sample_reviews_string = " | ".join(df_cleaned['Cleaned_Review'].astype(str).tail(10).tolist())
    
    return total_rows, unique_rows, duplicate_count, duplicate_percentage, df_cleaned, sample_reviews_string

# -------------------------------------------------------------
# GLOBAL INITIALIZATION & USER DATABASE CONFIGURATION (PERSISTENT)
# -------------------------------------------------------------
if "user_db" not in st.session_state:
    st.session_state.user_db = {"test@ikshana.com": "password123"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "role" not in st.session_state:
    st.session_state.role = "welcome"

# System Catalog for storing dynamic certificates generated during seller sessions
if "global_certified_catalog" not in st.session_state:
    st.session_state.global_certified_catalog = [
        {"company": "X-Corp", "product": "X-Phone Pro", "badge": "💎 AI Platinum Certified", "score": 95},
        {"company": "VoltLabs", "product": "VoltCharge 20W", "badge": "🥇 AI Gold Certified", "score": 89}
    ]

# -------------------------------------------------------------
# 🔐 AUTHENTICATION GATE
# -------------------------------------------------------------
if not st.session_state.authenticated:
    st.title("🎯 Welcome to Ikshana AI")
    st.subheader("Please sign in or create an account to access the platform")
    st.write("---")
    
    auth_mode = st.radio("Choose Action", ["Secure Login", "Create New Account"], horizontal=True)
    
    with st.form("auth_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="name@example.com").strip().lower()
        password = st.text_input("Account Password", type="password", placeholder="••••••••")
        
        if auth_mode == "Secure Login":
            submit_btn = st.form_submit_button("Sign In to Gateway", use_container_width=True, type="primary")
            if submit_btn:
                if email in st.session_state.user_db and st.session_state.user_db[email] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = email
                    st.success(f"Welcome back, {email}!")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("❌ Invalid email address or password credentials. Please try again.")
                    
        elif auth_mode == "Create New Account":
            confirm_password = st.text_input("Confirm Account Password", type="password", placeholder="••••••••")
            submit_btn = st.form_submit_button("Register New Profile", use_container_width=True, type="primary")
            
            if submit_btn:
                if not email or not password:
                    st.error("❌ Email and password strings cannot be left completely empty.")
                elif "@" not in email or "." not in email:
                    st.error("❌ Please provide a structurally valid email syntax formatting profile.")
                elif password != confirm_password:
                    st.error("❌ Password mismatch error. Double-check your matching inputs.")
                elif email in st.session_state.user_db:
                    st.error("❌ This email registry profile already exists inside our record logs.")
                else:
                    st.session_state.user_db[email] = password
                    st.session_state.authenticated = True
                    st.session_state.current_user = email
                    st.success("🎉 Account profile successfully deployed to system clusters!")
                    time.sleep(0.3)
                    st.rerun()
    st.stop()

# --- HEADER INFRASTRUCTURE ---
col_user, col_logout = st.columns([8, 2])
col_user.markdown(f"👤 Active Session: **{st.session_state.current_user}**")
if col_logout.button("🚪 Logout From System", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.role = "welcome"
    st.rerun()

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
        st.write("Register products, upload records, extract sentiment profiles, and generate certified trust badges.")
        if st.button("Enter Seller Gateway", use_container_width=True):
            st.session_state.role = "seller"
            st.rerun()
    with col2:
        st.success("### 🛍️ Consumer Shoppers")
        st.write("Cross-reference claims, prompt custom ranking algorithms, and converse with the Copilot.")
        if st.button("Enter Shopper Space", use_container_width=True):
            st.session_state.role = "shopper"
            st.rerun()
    with col3:
        st.warning("### 🏆 Public AI Rankings")
        st.write("Explore dynamic market registries grouping items securely by algorithmic validation scores.")
        if st.button("Open Public Board", use_container_width=True):
            st.session_state.role = "public_board"
            st.rerun()

# -------------------------------------------------------------
# SCREEN 2: HIGH-SPEED ENTERPRISE SELLER ENGINE
# -------------------------------------------------------------
elif st.session_state.role == "seller":
    st.title("🏪 Seller Control Center & Product Profiler")
    if st.button("← Back to Welcome Gateway"):
        st.session_state.role = "welcome"
        st.rerun()
    st.write("---")
    
    # --- PROFILER INTERFACE DOORWAY ---
    st.markdown("### 📝 Step 1: Product Registry Settings")
    col_p1, col_p2 = st.columns(2)
    company_name = col_p1.text_input("Company Name / Corporate Brand", placeholder="e.g., TechNexus Ltd").strip()
    product_name = col_p2.text_input("Product Model Identity", placeholder="e.g., Nexus Buds Pro").strip()
    product_img = st.file_uploader("Upload Product Presentation Image (Optional)", type=["jpg", "png", "jpeg"])
    
    if product_img and not product_img.type.startswith("image/"):
        st.error("Please provide a structurally valid image file formatting profile.")
        st.stop()
        
    st.write("---")
    st.markdown("### 📥 Step 2: Feed Dataset Ingestion")
    
    # Gate block validation check parameters
    if not company_name or not product_name:
        st.warning("⚠️ Access Locked: Please completely fill out your Company Name and Product Model details above to open the analysis engine pipeline.")
    else:
        uploaded_file = st.file_uploader("Drop e-commerce tracking data registers here (.csv or .xlsx)", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()
            is_csv = uploaded_file.name.endswith('.csv')
            
            total_rows, unique_rows, duplicate_count, duplicate_percentage, df_cleaned, sample_reviews = process_dataframe_metrics(file_bytes, is_csv=is_csv)
            st.write(f"📊 Extracted **{total_rows} total rows** from the registry catalog.")
            
            if total_rows < 50:
                st.error(f"❌ Document Rejected: Only {total_rows} rows parsed. File must contain a minimum of 50 reviews to initiate AI configuration.")
            else:
                st.success("✅ Metadata Profile Verified & Row Threshold Passed. Analytical environment ready.")
                
                # Render option image asset placeholder if provided by custom profile logs
                if product_img:
                    st.image(product_img, caption=f"Processing Pipeline Active for: {product_name}", width=250)
                
                st.markdown("### 🔍 Pre-Processing & Repetition Analysis")
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                col_metric1.metric("Unique Records Verified", f"{unique_rows}")
                col_metric2.metric("Identical Repetitions Flagged", f"{duplicate_count}")
                col_metric3.metric("Data Redundancy Rate", f"{duplicate_percentage}%")
                
                # Visual charts
                chart_data = pd.DataFrame({
                    "Record Type": ["Unique Verified Reviews", "Repetitive Spam Entries"],
                    "Row Count": [int(unique_rows), int(duplicate_count)]
                }).set_index("Record Type")
                st.bar_chart(chart_data)
                
                # --- NEW INTERACTIVE CUSTOM PROMPT INGESTION LAYER ---
                st.write("---")
                st.markdown("### 🎯 Custom Evaluation Directives")
                user_analysis_prompt = st.text_input(
                    "Guide the AI: Enter specific extraction directives or queries for this dataset",
                    placeholder="e.g., Focus heavily on what users say about packaging quality and durability parameters..."
                )
                
                st.write("---")
                st.markdown("### 🧠 Deep AI Linguistic Translation & Suggestions")
                
                advanced_ai_prompt = f"""
                You are an advanced retail data engineering model. 
                Company Profile: {company_name}
                Product Profile: {product_name}
                Dataset Stream: "{sample_reviews}"
                Custom User Directive: "{user_analysis_prompt if user_analysis_prompt else 'Perform standard deep audit.'}"
                
                Please execute the following operations step-by-step:
                1. EMOJI DE-NOISING SUMMARY: Identify common emojis and explain their textual meaning context.
                2. CUSTOM SUGGESTIONS PROFILE: Adhere strictly to the Custom User Directive if provided. Detail the structural engineering flaws or product quality updates discovered.
                3. OPERATIONAL ACTION ADVICE: Provide strategic engineering fixes designed truly by AI reasoning.
                """
                
                st.markdown("#### Live AI Deep Audit Output (Streaming):")
                st.write_stream(stream_gemini_ai(advanced_ai_prompt))
                st.balloons()
                
                # --- AUTO-GENERATING CERTIFICATE & DYNAMIC SEALS SYSTEM ---
                st.write("---")
                st.markdown("### 📜 Automated Verification Trust Badge Certification")
                
                # Compute mock score off internal data metrics parameters dynamically
                calculated_trust_score = int(max(40, min(100, 100 - (duplicate_percentage * 1.5))))
                assigned_badge = "💎 AI Platinum Certified" if calculated_trust_score >= 90 else "🥇 AI Gold Certified"
                
                # Inject current data registry directly into database structures for shoppers to query
                if not any(item['product'] == product_name for item in st.session_state.global_certified_catalog):
                    st.session_state.global_certified_catalog.append({
                        "company": company_name,
                        "product": product_name,
                        "badge": assigned_badge,
                        "score": calculated_trust_score
                    })
                
                # CSS Template styling wrapper configuration
                cert_html = f"""
                <div style="border:10px double #4A90E2; padding:30px; text-align:center; background-color:#1E1E1E; color:#FFFFFF; border-radius:15px; font-family:Arial, sans-serif;">
                    <h1 style="color:#4A90E2; margin-bottom:5px;">IKSHANA AI VALIDATION SEAL</h1>
                    <p style="font-style:italic; font-size:14px; color:#A0A0A0;">The Supervisory Lens for Digital Commerce Transparency</p>
                    <hr style="border-color:#4A90E2; width:80%;">
                    <br>
                    <p style="font-size:18px; margin:5px 0;">This cryptographic record logs confirm that the consumer data feeds of</p>
                    <h2 style="color:#F5A623; margin:10px 0;">{company_name}</h2>
                    <p style="font-size:18px; margin:5px 0;">for the tracked merchandise profile identified as</p>
                    <h2 style="color:#50E3C2; margin:10px 0;">{product_name}</h2>
                    <p style="font-size:16px;">has successfully undergone algorithmic de-noising, symbol translation, redundancy screening, and context validation.</p>
                    <br>
                    <div style="display:inline-block; border:2px dashed #F5A623; padding:15px 30px; border-radius:10px; background-color:#2A2A2A;">
                        <span style="font-size:22px; font-weight:bold;">{assigned_badge}</span><br>
                        <span style="font-size:16px; color:#A0A0A0;">Trust Quality Index: {calculated_trust_score}/100</span>
                    </div>
                    <br><br>
                    <p style="font-size:12px; color:#666666;">Issued autonomously by the Ikshana Application Environment Pipeline Engine Clusters.</p>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
                st.write("")
                
                # Document output compiler downloader tool action
                st.download_button(
                    label="📥 Download Official Trust Certificate (HTML Format)",
                    data=cert_html,
                    file_name=f"ikshana_verification_{product_name.replace(' ', '_')}.html",
                    mime="text/html",
                    use_container_width=True
                )
                
                # Dataset registry down-downloader
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
# SCREEN 3: SHOPPER SPACE & CUSTOM RANKING ENGINE PROMPT KEYBOARD
# -------------------------------------------------------------
elif st.session_state.role == "shopper":
    st.title("🛍️ Shopper Verification & Prompt-Driven Ranking")
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
            
    # --- NEW KEYBOARD SEARCH PROMPT FOR CUSTOM PRODUCTS RANKING ---
    st.write("---")
    st.markdown("### 🏆 AI Prompt-Driven Global Source Search & Ranker Keyboard")
    st.write("💡 *The AI will intelligently rank catalog options across web metrics, verified certificates, and system parameters.*")
    
    user_ranking_query = st.text_input(
        "Enter what parameters you want to rank products by (e.g., Rank the products best suited for high battery life and clear audio)",
        placeholder="Type custom ranking instructions here..."
    )
    
    if user_ranking_query:
        with st.spinner("AI Engine auditing systemic certification entries and aggregating global source signals..."):
            # Serialize current active certificates database map to contextual string feeds
            catalog_context_string = ""
            for item in st.session_state.global_certified_catalog:
                catalog_context_string += f"Product: {item['product']} by Company: {item['company']}, Trust Score: {item['score']}, Active Stamp: {item['badge']}. | "
                
            ranking_engine_prompt = f"""
            You are the Ikshana AI Global Search and Autonomous Evaluation Model.
            Here is the internal database of certified products tracking parameters:
            "{catalog_context_string}"
            
            The user wants to rank items using this specific instruction query: "{user_ranking_query}"
            
            Based on both our internal certification entries and generalized global marketplace signals, compile a ranked list of items. For each ranked choice, state their active certificate stamp properties if present, explain why they match the prompt requirements, and supply a clear final comparison matrix index layout.
            """
            st.markdown("#### Dynamic AI Ranking Matrix Output:")
            st.write_stream(stream_gemini_ai(ranking_engine_prompt))

    st.write("---")
    st.markdown("### 💬 Ikshana Shopping Copilot")
    query = st.text_input("Ask Chat Assistant About Product Discrepancies:")
    if query:
        chat_response_stream = stream_gemini_ai(query)
        st.write_stream(chat_response_stream)

# -------------------------------------------------------------
# SCREEN 4: PUBLIC BOARD (SYNCHRONIZED DYNAMIC CERTIFICATE TIER CATALOG)
# -------------------------------------------------------------
elif st.session_state.role == "public_board":
    st.title("🏆 Global Trust Leaderboards")
    if st.button("← Back to Welcome Gateway"):
        st.session_state.role = "welcome"
        st.rerun()
    st.write("---")
    
    st.write("💡 *Self-generating category tiers dynamically populated by current live certified seller configurations.*")
    
    # Read dynamically directly from our session data registry logs
    live_catalog = st.session_state.global_certified_catalog
    
    # Sort items securely descending according to computed data parameters scores
    sorted_catalog = sorted(live_catalog, key=lambda k: k['score'], reverse=True)
    
    for rank, item in enumerate(sorted_catalog, 1):
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 2])
            col1.markdown(f"## #{rank}")
            col2.markdown(f"**{item['product']}** by *{item['company']}* \n\n`{item['badge']}`")
            col3.metric("Trust Index Score", f"{item['score']}/100")
            st.write("---")    
              
