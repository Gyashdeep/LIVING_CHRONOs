import os
import time
import json
import streamlit as st
from groq import Groq

# --- HARDENED INITIALIZATION ---
def get_client():
    # Force check for secrets
    key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not key:
        st.error("FATAL: GROQ_API_KEY is missing from Streamlit Secrets.")
        st.stop()
    return Groq(api_key=key)

def get_instruction(client, vitals):
    """Direct call with minimal overhead."""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Vitals: {json.dumps(vitals)}. Output: 'ADJUST:50'"}],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        # This will reveal the exact cause of the THROTTLE
        return f"API_ERROR: {str(e)[:30]}"

# --- UI LAYER ---
def main():
    st.title("AXIOM-0: KERNEL ACTIVE")
    client = get_client()

    if 'next_run' not in st.session_state: st.session_state.next_run = 0

    if time.time() >= st.session_state.next_run:
        vitals = {"temp": 77.0, "status": "STABLE"}
        msg = get_instruction(client, vitals)
        
        st.write(f"DEBUG_OUTPUT: {msg}")
        
        if "ADJUST" in msg:
            st.success(f"SUCCESS: {msg}")
            st.session_state.next_run = time.time() + 30 # 2 requests per minute
        else:
            st.error(f"REFUSAL/THROTTLE: {msg}")
            st.session_state.next_run = time.time() + 60 # Cooldown
    else:
        st.info(f"Cooldown: {int(st.session_state.next_run - time.time())}s")
        time.sleep(2)
        st.rerun()

    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
