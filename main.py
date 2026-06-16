import os
import time
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
    st.title("AXIOM-0: QUANTUM KERNEL")
    client = get_client()

    # Minimal logic: Execute once, then pause silently
    if 'last_run' not in st.session_state:
        st.session_state.last_run = 0

    if time.time() - st.session_state.last_run > 30:
        instruction = get_instruction(client)
        if instruction and "ADJUST" in instruction:
            st.success("Quantum Link Established!")
            st.balloons()
            st.subheader(f"KERNEL RESPONSE: {instruction}")
            st.session_state.last_run = time.time()
        
    # No "Cooling down" text - just a silent wait
    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
