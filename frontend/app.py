import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="YouTube RAG", page_icon="🎬", layout="centered")

st.title("🎬 YouTube RAG")
st.caption("Ask questions about any YouTube video using its transcript.")

# --- Video Loader ---
st.subheader("Load a Video")

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Load Video", type="primary"):
    if not url.strip():
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching transcript and building index..."):
            try:
                res = requests.post(f"{API_BASE}/load", json={"youtube_url": url})
                data = res.json()
                if res.ok:
                    st.success(data.get("message", "Video loaded successfully!"))
                    st.session_state.loaded_url = url
                    st.session_state.messages = []
                else:
                    st.error(data.get("detail", "Failed to load video."))
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

# --- Chat Section ---
if "loaded_url" in st.session_state:
    st.divider()
    st.subheader("Ask a Question")
    st.caption(f"Loaded: `{st.session_state.loaded_url}`")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Question input
    question = st.chat_input("Ask something about the video...")

    if question:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(f"{API_BASE}/ask", json={
                        "youtube_url": st.session_state.loaded_url,
                        "question": question
                    })
                    data = res.json()
                    if res.ok:
                        answer = data.get("answer", "No answer returned.")
                    else:
                        answer = f"Error: {data.get('detail', 'Something went wrong.')}"
                except Exception as e:
                    answer = f"Could not connect to backend: {e}"

                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})