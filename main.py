import os
import time
import json
import streamlit as st
from groq import Groq, RateLimitError

@st.cache_resource
def get_axiom_controller():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set.")
    return AxiomZero(api_key)

class HardwareInterface:
    def write(self, data: str):
        # We strip everything except the requested format to keep the output clean
        clean_data = data.strip().replace("CMD:", "")
        st.write(f" [OUTPUT] >> {clean_data}")

class AxiomZero:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.io = HardwareInterface()

    def sovereign_thought(self, vitals):
        # The prompt is now focused on data mapping, not 'code'
        prompt = f"System Vitals: {json.dumps(vitals)}. Map this to a cooling state. Output ONLY the string 'ADJUST:X' where X is a value from 0 to 100."
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a data formatting engine. Respond only with the requested 'ADJUST:X' string format. Do not use code blocks or explanations."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.0
            )
            return response.choices[0].message.content
        except Exception:
            return "ERROR_THROTTLE"

def main():
    st.title("AXIOM-0: QUANTUM KERNEL")
    axiom = get_axiom_controller()
    
    if 'last_run' not in st.session_state: st.session_state.last_run = 0

    while True:
        if time.time() - st.session_state.last_run >= 15:
            vitals = {"temp": 77.0, "status": "STABLE"}
            msg = axiom.sovereign_thought(vitals)
            axiom.io.write(msg)
            st.session_state.last_run = time.time()
        time.sleep(1)

if __name__ == "__main__":
    main()
