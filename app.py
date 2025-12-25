# --- 1. DEPLOYMENT FIX (Must remain at top) ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ----------------------------------------------

import streamlit as st
import os
from dotenv import load_dotenv
import backend  # Import our new logic file

# 2. Config
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Orbit 🪐", page_icon="🪐", layout="wide")

# 3. Initialize Session State
if "vector_store" not in st.session_state:
    st.session_state.vector_store = backend.get_vector_store()

# --- FIX: Set the Greeting ONE TIME at startup ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm Orbit! The AI assistant for CollabCircle. How may I help you?"}
    ]

# --- UI: Header ---
st.title("Orbit 🪐")
st.caption("The Knowledge Hub for CollabCircle")

# --- UI: Sidebar (Admin Mode) ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Check if Brain is loaded
    if st.session_state.vector_store:
        st.success("🟢 System Online")
    else:
        st.error("🔴 Brain Missing")

    # Admin Panel
    with st.expander("Admin: Update Knowledge"):
        password = st.text_input("Admin Password", type="password")
        if password == "collab123": # Simple lock mechanism
            uploaded_files = st.file_uploader("Upload New Research", type="pdf", accept_multiple_files=True)
            if st.button("Update Database"):
                if uploaded_files:
                    with st.spinner("Processing..."):
                        st.session_state.vector_store = backend.update_knowledge_base(uploaded_files)
                        st.success("Database Updated!")

# --- UI: Chat Loop ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about CollabCircle..."):
    # Add User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    if st.session_state.vector_store:
        try:
            rag_chain = backend.get_rag_chain(st.session_state.vector_store)
            
            with st.spinner("Accessing CollabCircle Archives..."):
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"]

            # Add AI Message
            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Orbit is offline. Please initialize the knowledge base.")