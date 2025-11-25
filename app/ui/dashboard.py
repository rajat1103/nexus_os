import streamlit as st
import httpx
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS OS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CUSTOM CSS (THE "HACK") ---
st.markdown("""
    <style>
        /* Import Futuristic Font */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;400&display=swap');

        /* GLOBAL THEME */
        .stApp {
            background-color: #0e1117;
            background-image: radial-gradient(circle at 50% 50%, #1c2331 0%, #0e1117 100%);
            color: #e0e0e0;
            font-family: 'Roboto Mono', monospace;
        }

        /* HEADERS */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00e5ff !important;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
        }

        /* SIDEBAR STYLING */
        [data-testid="stSidebar"] {
            background-color: #0a0c10;
            border-right: 1px solid #1f2937;
        }

        /* CUSTOM BUTTONS */
        .stButton>button {
            background: linear-gradient(45deg, #00b4db, #0083b0);
            color: white;
            border: none;
            border-radius: 4px;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 15px rgba(0, 180, 219, 0.6);
        }

        /* CHAT BUBBLES - USER */
        [data-testid="stChatMessage"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* CHAT INPUT */
        .stTextInput>div>div>input {
            background-color: #1f2937;
            color: #00e5ff;
            border: 1px solid #374151;
            font-family: 'Roboto Mono', monospace;
        }
        
        /* SCROLLBAR */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0e1117; 
        }
        ::-webkit-scrollbar-thumb {
            background: #374151; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00e5ff; 
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_status" not in st.session_state:
    st.session_state.system_status = "ONLINE"

# --- 4. SIDEBAR (CONTROL PANEL) ---
with st.sidebar:
    st.title("NEXUS /// OS")
    st.markdown("---")
    
    # System Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="CPU", value="12%", delta="-2%")
    with col2:
        st.metric(label="RAM", value="4.2GB", delta="+0.1GB")
    
    st.markdown("### 📥 Neural Ingestion")
    with st.container():
        category = st.selectbox("Data Classification", ["PROTOCOL", "RESEARCH", "PERSONAL", "CODEBASE"])
        new_memory = st.text_area("Input Raw Data", height=150, placeholder="Paste classified documents here...")
        
        if st.button("UPLOAD TO CORTEX", use_container_width=True):
            if new_memory:
                try:
                    with st.spinner("Encrypting & Vectorizing..."):
                        response = httpx.post(
                            "http://localhost:8000/learn", 
                            json={"content": new_memory, "category": category},
                            timeout=10.0
                        )
                    if response.status_code == 200:
                        st.success(":: DATA ASSIMILATED ::")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f":: UPLOAD FAILED :: {response.text}")
                except Exception as e:
                    st.error(f"Network Severed: {str(e)}")

    st.markdown("---")
    st.markdown(f"**Status:** `{st.session_state.system_status}`")
    st.markdown("**Version:** `v0.8.2-Alpha`")

# --- 5. MAIN CHAT INTERFACE ---
st.markdown("## NEURAL INTERFACE")

# Display History
for message in st.session_state.messages:
    role_icon = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=role_icon):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Enter Command..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. AI Response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("Analyzing Neural Pathways..."):
                # Call Backend
                api_response = httpx.post(
                    "http://localhost:8000/chat", 
                    json={"query": prompt},
                    timeout=30.0
                )
                
                if api_response.status_code == 200:
                    data = api_response.json()
                    ai_text = data["response"]
                    sources = data.get("source_context", [])
                    
                    # Display Text
                    message_placeholder.markdown(ai_text)
                    
                    # Display Sources nicely
                    if sources and sources[0]:
                        with st.expander("🔍 SOURCE FRAGMENTS DETECTED"):
                            for idx, src in enumerate(sources[0]):
                                st.code(src, language="text")
                                
                    st.session_state.messages.append({"role": "assistant", "content": ai_text})
                    
                else:
                    error_msg = f"SYSTEM ERROR [Code {api_response.status_code}]"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except Exception as e:
            error_msg = f"CRITICAL FAILURE: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})