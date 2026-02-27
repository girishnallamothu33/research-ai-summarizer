import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import time

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="Transform Complex Research into Clear Knowledge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark SaaS Theme
st.markdown("""
    <style>
    /* Dark Theme & Glassmorphism */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stSidebar {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(110, 69, 226, 0.4);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2428;
        border-radius: 4px;
        padding: 5px 15px;
    }
    .css-1d391kg {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #58a6ff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Transform Complex Research into Clear Knowledge")
st.markdown("Upload a research paper, select your discipline, and extract actionable insights effortlessly.")

with st.sidebar:
    st.header("⚙️ Settings")
    discipline = st.selectbox(
        "Select Discipline context",
        ("General", "AI", "Medical", "Physics", "Economics", "Biology")
    )
    st.markdown("---")
    st.subheader("📊 History")
    if st.button("Refresh History"):
        try:
            hist_res = requests.get(f"{API_BASE_URL}/history")
            if hist_res.status_code == 200:
                history = hist_res.json()
                if len(history) == 0:
                    st.info("No history found.")
                for item in history:
                    st.text(f"• {item['filename']} ({item['discipline']})")
            else:
                st.error("Failed to load history")
        except:
            st.error("Backend offline")

# Main content
col1, col2 = st.columns([1, 1])

extracted_text = ""

with col1:
    st.subheader("1. Setup Input")
    uploaded_file = st.file_uploader("Upload PDF Paper", type="pdf")
    manual_text = st.text_area("Or Paste Abstract/Text", height=250)

    if st.button("Extract Text from PDF") and uploaded_file:
        with st.spinner("Extracting text via PyPDF2..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                res = requests.post(f"{API_BASE_URL}/upload", files=files)
                if res.status_code == 200:
                    st.success("Text extracted successfully!")
                    st.session_state['extracted_text'] = res.json()["extracted_text"]
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

    if 'extracted_text' in st.session_state:
        st.text_area("Extracted Preview", st.session_state['extracted_text'][:1000] + "...", height=150, disabled=True)
        extracted_text = st.session_state['extracted_text']
        
    if manual_text:
        extracted_text = manual_text

with col2:
    st.subheader("2. Generate Insights")
    if st.button("Generate Insights", use_container_width=True):
        if not extracted_text:
            st.warning("Please upload a PDF or paste text first.")
        else:
            with st.spinner("Analyzing text with AI models..."):
                try:
                    payload = {"text": extracted_text, "discipline": discipline}
                    res = requests.post(f"{API_BASE_URL}/summarize", json=payload)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.toast("Analysis Complete!", icon="✅")
                        
                        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Short Summary", "Detailed Summary", "Keywords", "Key Insights", "Discipline Focus"])
                        
                        with tab1:
                            st.write(data.get("short_summary", "N/A"))
                        with tab2:
                            st.write(data.get("detailed_summary", "N/A"))
                        with tab3:
                            keywords = data.get("keywords", [])
                            st.write(", ".join([f"`{k}`" for k in keywords]))
                        with tab4:
                            for ins in data.get("key_insights", []):
                                st.markdown(f"- {ins}")
                        with tab5:
                            st.info(data.get("discipline_interpretation", "N/A"))
                            
                        # Demo Clustering visualization
                        st.subheader("Topic Clustering Visualization")
                        # Split text into sentences for demo clustering
                        sentences = [s for s in extracted_text.split('.') if len(s) > 20][:15]
                        if sentences:
                            cluster_res = requests.post(f"{API_BASE_URL}/cluster", json={"texts": sentences})
                            if cluster_res.status_code == 200:
                                cluster_data = cluster_res.json().get("clusters", [])
                                df = pd.DataFrame(cluster_data)
                                if not df.empty:
                                    fig = px.scatter(
                                        df, x="x", y="y", color="cluster", 
                                        hover_data=["text"],
                                        title="Sentence Embeddings Cluster",
                                        template="plotly_dark",
                                        color_continuous_scale=px.colors.sequential.Plasma
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"API Error: {res.text}")
                except Exception as e:
                    st.error(f"Backend connection failed: {e}")
