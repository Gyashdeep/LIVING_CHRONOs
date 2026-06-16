import os
import time
import json
import streamlit as st
from groq import Groq

@st.cache_resource
def get_client():
    key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    return Groq(api_key=key)

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
    st.title("AXIOM-0: KERNEL ACTIVE")
    client = get_client()

    if 'last_run' not in st.session_state: st.session_state.last_run = 0

    elapsed = time.time() - st.session_state.last_run
    
    # Logic to trigger update every 30 seconds
    if elapsed > 30:
        instruction = get_instruction(client)
        if instruction and "ADJUST" in instruction:
            st.session_state.last_instruction = instruction
            st.session_state.last_run = time.time()
            st.success(f"NEW INSTRUCTION: {instruction}")
        else:
            st.warning("API call failed or empty.")
    else:
        st.info(f"System cooling. Next cycle in: {int(30 - elapsed)} seconds.")
        if 'last_instruction' in st.session_state:
            st.write(f"Current State: {st.session_state.last_instruction}")
        
        time.sleep(2)
        st.rerun()

    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
