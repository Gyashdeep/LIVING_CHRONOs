import os
import time
import json
import streamlit as st
from groq import Groq

@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY"))

def get_instruction(client):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Return the string 'ADJUST:50' only."}],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception:
        return None

def main():
    st.title("AXIOM-0: QUANTUM LINK ACTIVE")
    client = get_client()

    # Simple 20-second interval logic
    if 'next_run' not in st.session_state: st.session_state.next_run = 0

    if time.time() >= st.session_state.next_run:
        instruction = get_instruction(client)
        if instruction:
            st.success(f"INSTRUCTION: {instruction}")
            st.session_state.next_run = time.time() + 20 # 20s interval
        else:
            st.warning("Connection lost. Retrying in 60s...")
            st.session_state.next_run = time.time() + 60
    else:
        st.info(f"Stasis. Next update: {int(st.session_state.next_run - time.time())}s")
        time.sleep(2)
        st.rerun()

    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
