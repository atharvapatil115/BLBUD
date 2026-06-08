import streamlit as st
import base64
import time

from dotenv import load_dotenv
load_dotenv()

from src.retrieval.retriever import Retriever, build_context
from src.llm.mistral import MistralLLM


# ✅ Page config
st.set_page_config(
    page_title="Belfius Buddy",
    page_icon="🤖",
    layout="wide"
)


# ✅ Convert logo to base64
def get_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64("assets/logo.png")


# ✅ ✅ STARTUP LOADER
if "app_loaded" not in st.session_state:

    st.markdown("""
    <style>
    .startup-loader {
        position: fixed;
        inset: 0;
        background: #242124;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    .buddy-circle {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: linear-gradient(135deg, #c30045, #ff4b7d);
        animation: pulseGlow 2s infinite;
        position: relative;
    }

    .buddy-circle::after {
        content: '';
        position: absolute;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 3px solid #ff4b7d;
        top: -15px;
        left: -15px;
        animation: ripple 2s infinite;
    }

    @keyframes pulseGlow {
        0% { transform: scale(1); box-shadow: 0 0 10px rgba(255,75,125,0.4); }
        50% { transform: scale(1.2); box-shadow: 0 0 30px rgba(255,75,125,0.9); }
        100% { transform: scale(1); box-shadow: 0 0 10px rgba(255,75,125,0.4); }
    }

    @keyframes ripple {
        0% { transform: scale(0.8); opacity: 0.6; }
        100% { transform: scale(1.6); opacity: 0; }
    }

    .loader-text {
        margin-top: 20px;
        font-size: 18px;
        color: #ff4b7d;
        font-weight: 600;
        animation: fade 1.5s infinite;
    }

    @keyframes fade {
        0%,100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    </style>

    <div class="startup-loader">
        <div class="buddy-circle"></div>
        <div class="loader-text">Launching Belfius Buddy...</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(3.5)
    st.session_state.app_loaded = True
    st.rerun()


# ✅ ✅ MAIN UI CSS (FIXED ANIMATION HERE)
st.markdown(f"""
<style>

/* ✅ GLOBAL APP ANIMATION (FIXED WAY) */
[data-testid="stAppViewContainer"] {{
    animation: smoothEntry 0.9s cubic-bezier(0.22, 1, 0.36, 1);
}}

@keyframes smoothEntry {{
    0% {{
        opacity: 0;
        transform: translateY(40px) scale(0.96);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

/* ✅ Background */
html, body {{
    background-color: #242124 !important;
    color: white !important;
}}

/* ✅ Header */
header[data-testid="stHeader"] {{
    background-color: #c30045 !important;
    height: 70px;
}}

/* ✅ Header center */
.header-center {{
    position: fixed;
    top: 15px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    z-index: 999;
}}

.header-center img {{
    height: 40px;
    margin-right: 10px;
}}

.header-center span {{
    font-size: 22px;
    font-weight: bold;
    color: white;
}}

/* ✅ Sidebar */
section[data-testid="stSidebar"] {{
    background-color: rgba(195, 0, 69, 0.96) !important;
    border: 2px solid black !important;
}}

/* ✅ Chat */
.stChatMessage[data-testid="stChatMessage-user"] {{
    background-color: #c30045 !important;
    color: white !important;
    border-radius: 16px;
    padding: 12px;
}}

.stChatMessage[data-testid="stChatMessage-assistant"] {{
    background-color: #f5f5f5 !important;
    color: black !important;
    border-radius: 16px;
    padding: 12px;
}}

.main-spacing {{
    margin-top: 80px;
}}

</style>
""", unsafe_allow_html=True)


# ✅ ✅ HEADER (FIXED IMAGE)
st.markdown(f"""
<div class="header-center">
    <img src="data:image/png;base64,{logo_base64}">
    <span>Belfius <span style="color:#ff4b7d;">Buddy</span></span>
</div>
""", unsafe_allow_html=True)


# ✅ spacing
st.markdown('<div class="main-spacing"></div>', unsafe_allow_html=True)


# ✅ Components
@st.cache_resource
def load_components():
    retriever = Retriever(
        index_path="data/vector_store/index.faiss",
        metadata_path="data/vector_store/metadata.pkl",
    )
    llm = MistralLLM()
    return retriever, llm

retriever, llm = load_components()


# ✅ Subtitle
st.markdown("### Ask questions related to Belfius")


# ✅ Sidebar
with st.sidebar:
    st.image("assets/bg.png", width=250)
    st.markdown("<h1 style='color:white;'>Buddy</h1>", unsafe_allow_html=True)

    top_k = st.slider("Top K Results", 1, 10, 5)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []


# ✅ Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# ✅ Show chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ✅ Input
query = st.chat_input("Ask something...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        results = retriever.search(query=query, top_k=top_k)
        context = build_context(results)
        answer = llm.generate(query=query, context=context)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.expander("🔍 Retrieved Context"):
        st.write(context)