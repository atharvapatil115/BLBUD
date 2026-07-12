import streamlit as st
import base64
import time

from dotenv import load_dotenv
load_dotenv()

# ✅ MODELS
from app.models.user import User
from app.models.company_user import CompanyUser
from app.models.chat import Chat
from app.models.message import Message

# ✅ DB
from app.db.database import Base, engine, SessionLocal

# ✅ AUTH
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_token, verify_token

# ✅ RAG
from src.retrieval.retriever import Retriever, build_context
from src.llm.mistral import MistralLLM


# ✅ INIT DB
Base.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()


def get_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_base64("assets/logo.png")


# ✅ AUTH
def signup_user(email, password):
    db = get_db()

    if db.query(User).filter(User.email == email).first():
        return False, "User already exists"

    if not db.query(CompanyUser).filter(CompanyUser.email == email).first():
        return False, "You are not authorized (not a company user)"

    user = User(email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()

    return True, "Account created ✅"


def login_user(email, password):
    db = get_db()
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    return create_token({"user_id": user.id, "email": user.email})


# ✅ SESSION
if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None


# ✅ LOGIN SCREEN (styled same)
if not st.session_state.token:

    st.markdown('<div class="main-spacing"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.05);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0px 0px 30px rgba(255,75,125,0.2);
            text-align: center;">
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <img src="data:image/png;base64,{logo_base64}" width="200">
        """, unsafe_allow_html=True)

        mode = st.radio("", ["Login", "Signup"], horizontal=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if mode == "Signup":
            if st.button("Create Account"):
                success, msg = signup_user(email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
        else:
            if st.button("Login"):
                token = login_user(email, password)

                if token:
                    st.session_state.token = token
                    st.session_state.user = verify_token(token)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ✅ PAGE CONFIG
st.set_page_config(page_title="Belfius Buddy", page_icon="🤖", layout="wide")






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
# ✅ HEADER WITH USER + LOGOUT
col1, col2, col3 = st.columns([3, 4, 2])



with col1:
    st.markdown("""
    <h3 style="text-align:center; color:white;">
        Belfius <span style="color:#ff4b7d;">Buddy</span>
    </h3>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align:left; font-size:14px;">
        👤 {st.session_state.user['email']}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.current_chat_id = None
        st.rerun()



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
    </style>

    <div class="startup-loader">
        Launching Belfius Buddy...
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="main-spacing"></div>', unsafe_allow_html=True)


# ✅ LOAD COMPONENTS
@st.cache_resource
def load_components():
    return (
        Retriever("data/vector_store/index.faiss","data/vector_store/metadata.pkl"),
        MistralLLM()
    )

retriever, llm = load_components()


db = get_db()
user_id = st.session_state.user["user_id"]


# ✅ AUTO CREATE CHAT
if not st.session_state.current_chat_id:
    chat = db.query(Chat).filter(Chat.user_id == user_id).first()
    if chat:
        st.session_state.current_chat_id = chat.id
    else:
        new_chat = Chat(user_id=user_id, title="New Chat")
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        st.session_state.current_chat_id = new_chat.id


# ✅ SIDEBAR
with st.sidebar:
    st.image("assets/bg.png", width=250)

    if st.button("➕ New Chat"):
        new = Chat(user_id=user_id, title="New Chat")
        db.add(new)
        db.commit()
        db.refresh(new)
        st.session_state.current_chat_id = new.id
        st.rerun()

    chats = db.query(Chat).filter(Chat.user_id == user_id).all()

    for chat in chats:
        if st.button(chat.title, key=f"chat{chat.id}"):
            st.session_state.current_chat_id = chat.id
            st.rerun()


# ✅ SHOW MESSAGES
messages = db.query(Message)\
    .filter(Message.chat_id == st.session_state.current_chat_id)\
    .order_by(Message.id).all()

for msg in messages:
    with st.chat_message(msg.role):
        st.markdown(msg.content)


# ✅ INPUT
query = st.chat_input("Ask something...")

if query:
    chat_id = st.session_state.current_chat_id

    db.add(Message(chat_id=chat_id, role="user", content=query))
    db.commit()

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        results = retriever.search(query=query, top_k=5)
        context = build_context(results)
        answer = llm.generate(query=query, context=context)
        st.markdown(answer)

    db.add(Message(chat_id=chat_id, role="assistant", content=answer))
    db.commit()

    if db.query(Chat).get(chat_id).title == "New Chat":
        chat = db.query(Chat).get(chat_id)
        chat.title = query[:25]
        db.commit()

    st.rerun()


