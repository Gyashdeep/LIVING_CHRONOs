import os
import time
import json
import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
@st.cache_resource
def get_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY missing.")
    return Groq(api_key=api_key)

def get_instruction(client, vitals):
    """Call the LLM with a safe, direct prompt."""
    prompt = f"Vitals: {json.dumps(vitals)}. Output ONLY the string 'ADJUST:X' where X is 0-100."
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a controller. Respond only with 'ADJUST:X' format."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception:
        return None

# --- UI LAYER ---
def main():
    st.title("AXIOM-0: KERNEL ONLINE")
    client = get_client()

    # Initialize state
    if 'next_run' not in st.session_state:
        st.session_state.next_run = 0

    # Logic Loop
    if time.time() >= st.session_state.next_run:
        vitals = {"temp": 77.0, "status": "STABLE"}
        instruction = get_instruction(client, vitals)
        
        if instruction and "ADJUST" in instruction:
            st.success(f"INSTRUCTION RECEIVED: {instruction}")
            st.session_state.next_run = time.time() + 20
        else:
            st.warning("API Throttled or Refused. Cooldown...")
            st.session_state.next_run = time.time() + 60
    else:
        st.info(f"System in stasis. Next cycle in {int(st.session_state.next_run - time.time())}s")
        time.sleep(2)
        st.rerun()

    time.sleep(2)
    st.rerun()

if __name__ == "__main__":
    main()
    
