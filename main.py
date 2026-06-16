import os
import time
import json
import streamlit as st
from groq import Groq

# --- CORE LOGIC ---
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY"))

def get_sovereign_instruction(client, vitals):
    """Encapsulated API call with minimal overhead."""
    prompt = f"Vitals: {json.dumps(vitals)}. Output ONLY 'ADJUST:X' (X=0-100)."
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception:
        return None

# --- UI & STATE LAYER ---
def main():
    st.title("AXIOM-0: KERNEL ONLINE")
    client = get_client()

    # Session State tracks the timing to avoid hitting rate limits
    if 'next_run' not in st.session_state:
        st.session_state.next_run = time.time()

    if time.time() >= st.session_state.next_run:
        vitals = {"temp": 77.0, "status": "STABLE"}
        instruction = get_sovereign_instruction(client, vitals)
        
        if instruction:
            st.success(f"INSTRUCTION: {instruction}")
            st.session_state.next_run = time.time() + 20 # Wait 20 seconds between runs
        else:
            st.warning("API Throttled. Cooling down...")
            st.session_state.next_run = time.time() + 60 # Penalty cooldown
    else:
        st.info(f"System in stasis. Next cycle in {int(st.session_state.next_run - time.time())}s")
        time.sleep(2)
        st.rerun()

    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
