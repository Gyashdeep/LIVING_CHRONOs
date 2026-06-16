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
    except Exception as e:
        return None

def main():
    st.title("AXIOM-0: QUANTUM LINK ACTIVE")
    client = get_client()

    # We use session state to enforce a 30-second wait to be absolutely safe with your quota
    if 'last_run' not in st.session_state: st.session_state.last_run = 0

    if time.time() - st.session_state.last_run > 30:
        instruction = get_instruction(client)
        if instruction and "ADJUST" in instruction:
            st.success(f"KERNEL RESPONSE: {instruction}")
            st.session_state.last_run = time.time()
        else:
            st.warning("Awaiting next cycle...")
    else:
        st.info(f"System cooling: {30 - int(time.time() - st.session_state.last_run)}s remaining.")
        time.sleep(2)
        st.rerun()

    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()
