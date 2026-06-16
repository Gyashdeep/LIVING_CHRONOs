import os
import time
import json
import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
@st.cache_resource
def get_client():
    key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not key:
        st.error("FATAL: GROQ_API_KEY is missing.")
        st.stop()
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
        return f"ERROR: {str(e)}"

# --- UI LAYER ---
def main():
    st.title("AXIOM-0: QUANTUM KERNEL")
    client = get_client()

    st.write("Initializing link...")
    
    # Run the instruction fetch
    instruction = get_instruction(client)
    
    if instruction and "ADJUST" in instruction:
        # Success flow
        st.success("Quantum Link Established!")
        st.balloons()  # Visual confirmation
        st.subheader(f"KERNEL RESPONSE: {instruction}")
    else:
        # Error flow
        st.error(f"KERNEL REFUSAL/ERROR: {instruction}")

if __name__ == "__main__":
    main()
