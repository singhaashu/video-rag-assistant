import streamlit as st
from utils.audioprocessor import process_input
from core.trans_script import  transilble_all_chunk  # adjust import paths to match your project
from core.vectordb import build_vector, load_vector
from core.rag_engine import ask_question

st.set_page_config(page_title="Video Brief", page_icon="🎬")

st.title("🎬 Video Brief")
st.caption("Summarize any video and ask questions about it.")

# --- Sidebar: input video link ---
st.sidebar.header("Video Source")
url = st.sidebar.text_input("Paste your video link")
process_btn = st.sidebar.button("Process Video", use_container_width=True)

# --- Session state to avoid reprocessing on every rerun ---
if "vector" not in st.session_state:
    st.session_state.vector = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# --- Process video only when button is clicked ---
if process_btn:
    if not url:
        st.sidebar.error("Please paste a video link first.")
    else:
        with st.spinner("Downloading and processing audio..."):
            audio = process_input(url)

        with st.spinner("Transcribing and summarizing..."):
            summary = transilble_all_chunk(audio)
            st.session_state.summary = summary

        with st.spinner("Building knowledge base..."):
            build_vector(summary)
            st.session_state.vector = load_vector()

        st.sidebar.success("Video processed! You can now ask questions below.")

# --- Show summary if available ---
if st.session_state.summary:
    with st.expander("📄 View Summary"):
        st.write(st.session_state.summary)

# --- Question answering ---
st.subheader("Ask a question about the video")
question = st.text_input("Your question")
ask_btn = st.button("Get Answer")

if ask_btn:
    if st.session_state.vector is None:
        st.warning("Please process a video first (use the sidebar).")
    elif not question:
        st.warning("Please type a question.")
    else:
        with st.spinner("Thinking..."):
            response = ask_question(st.session_state.vector, question)
        st.markdown("### Answer")
        st.write(response)