import streamlit as st
import tempfile
import os
from resume_processing import extract_text_from_pdf
from roast_generator import generate_roast

st.set_page_config(layout="wide")

def load_css():
    with open("style.css", "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

st.title("🔥 AI Roast My Resume 🔥")

if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None

with st.chat_message("ai"):
    st.markdown('<div class="stChatMessageAI"><b>Hey there! 👋 </b>  Upload your resume, and I\'ll absolutely destroy it. 😈🔥</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

if uploaded_file:

    if "roast_generated" not in st.session_state:
        st.session_state["roast_generated"] = False

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name

        extracted_text = extract_text_from_pdf(temp_path)
        
        os.remove(temp_path)

    except Exception as e:
        st.error(f"❌ ERROR: {str(e)}")
        if os.path.exists(temp_path):  
            os.remove(temp_path)

    with st.chat_message("ai"):
        st.markdown('<div class="stChatContainer"><div class="stChatMessageAI"> <b> Oh wow... this is going to be fun 😂 </b> </div></div>', unsafe_allow_html=True)

    roast_output, feedback_output, summary_output = generate_roast(extracted_text)

    st.session_state["roast_generated"] = True

    with st.chat_message("ai"):
        st.markdown('<div class="roast-header"><b>Here\'s your short roast 🔥 :</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="roast-box">{summary_output}</div>', unsafe_allow_html=True)


    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Full Roast 🔥"):
            st.session_state["selected_option"] = "roast"

    with col2:
        if st.button("💡 Constructive Feedback"):
            st.session_state["selected_option"] = "feedback"

    if st.session_state["selected_option"] == "roast":
        with st.chat_message("ai"):
            st.markdown('<div class="roast-header"><b>Here\'s your full brutal roast 🔥:</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="roast-box">{roast_output}</div>', unsafe_allow_html=True)
    
        if st.button("💡 Okay, now give me feedback"):
            st.session_state["selected_option"] = "feedback"

    elif st.session_state["selected_option"] == "feedback":
        with st.chat_message("ai"):
            st.markdown('<div class="roast-header"><b>Here\'s your constructive feedback 💡:</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="roast-box">{feedback_output}</div>', unsafe_allow_html=True)

        if st.button("Actually, brutally roast me 💀!"):
            st.session_state["selected_option"] = "roast"
