import os
import time
import json
import streamlit as st
from groq import Groq

# --- FORCE RESET INITIALIZATION ---
@st.cache_resource
def get_client():
    key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not key:
        st.error("FATAL: GROQ_API_KEY is missing. Check Streamlit Secrets.")
        st.stop()
    return Groq(api_key=key)

def get_instruction(client):
    """Direct, single-shot request to bypass all state logic."""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Return the string 'ADJUST:50' only."}],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"

# --- UI LAYER ---
def main():
    st.title("AXIOM-0: FORCED REBOOT")
    client = get_client()

    # CLEAR ALL STATES: This line forces the app to ignore previous 'cooldowns'
    st.session_state.clear() 
    
    st.write("System attempting one-time connection...")
    
    instruction = get_instruction(client)
    
    if instruction and "ADJUST" in instruction:
        st.success(f"KERNEL RESPONSE: {instruction}")
        st.balloons()
    else:
        st.error(f"KERNEL REFUSAL/ERROR: {instruction}")
        st.write("Check Groq console for usage limits. If limit is 0, wait for daily reset.")

if __name__ == "__main__":
    main()
