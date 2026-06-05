import streamlit as st
import os
import base64

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


# ✅ CSS + HEADER UI
st.markdown(f"""
<style>

/* ✅ Page background */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: #242124 !important;
    color: white !important;
}}

/* ✅ Header styling */
header[data-testid="stHeader"] {{
    background-color: #c30045 !important;
    height: 70px;
}}

/* ✅ Center header content */
.header-center {{
    position: fixed;
    top: 15px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    z-index: 999;
}}

/* ✅ Logo */
.header-center img {{
    height: 40px;
    margin-right: 10px;
}}

/* ✅ Title */
.header-center span {{
    font-size: 22px;
    font-weight: bold;
    color: white;
}}

/* ✅ Sidebar */
section[data-testid="stSidebar"] {{
    background-color: rgba(195, 0, 69, 0.96) !important;
    color: white !important;
    border: 2px solid #000000 !important;
}}

/* ✅ Chat styles */
textarea {{
    color: white !important;
}}

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

/* ✅ Buttons */
.stButton > button {{
    background-color: #c30045;
    color: white;
    border-radius: 8px;
}}

/* ✅ Slider */
.stSlider [role="slider"] {{
    background-color: white !important;
}}

/* ✅ Push content below header */
.main-spacing {{
    margin-top: 80px;
}}

</style>
""", unsafe_allow_html=True)


# ✅ Inject center header logo + title
st.markdown(f"""
<div class="header-center">
    <img src="data:image/png;base64,{logo_base64}">
    <span>Belfius <span style="color:#ff4b7d;">Buddy</span></span>
</div>
""", unsafe_allow_html=True)


# ✅ spacing
st.markdown('<div class="main-spacing"></div>', unsafe_allow_html=True)


# ✅ Load components
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
st.markdown("### Ask questions related to belfius")


# ✅ Sidebar
with st.sidebar:

    # ✅ FIXED deprecated warning
    st.image("assets/bg.png", width=250)
        
    st.markdown("""
                 <h1 style="color:white; margin-top:5px;">Buddy</h1>
         """, unsafe_allow_html=True)

 
    top_k = st.slider("Top K Results", 1, 10, 5)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []


# ✅ Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# ✅ Show messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ✅ Input
query = st.chat_input("Ask something...")

if query:

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            results = retriever.search(
                query=query,
                top_k=top_k
            )

            context = build_context(results)

            answer = llm.generate(
                query=query,
                context=context
            )

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # ✅ Debug
    with st.expander("🔍 Retrieved Context"):
        st.write(context)