import os
import time
import json
import streamlit as st
from groq import Groq, RateLimitError

# --- CACHED INITIALIZATION ---
@st.cache_resource
def get_axiom_controller():
    """Ensures only one instance of the controller runs regardless of UI reruns."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set.")
    return AxiomZero(api_key)

class HardwareInterface:
    def __init__(self):
        self.use_hardware = os.environ.get("DEPLOY_ENV") == "LOCAL"
        self.ser = None
        if self.use_hardware:
            try:
                import serial
                self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            except Exception:
                pass

    def write(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data.strip()}\n".encode())
        else:
            st.write(f" [MOCK SERIAL] >> {data.strip()}")

class AxiomZero:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.io = HardwareInterface()

    def sovereign_thought(self, vitals):
        prompt = f"System Vitals: {json.dumps(vitals)}. Output only machine-code instructions."
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.05
            )
            return response.choices[0].message.content
        except RateLimitError:
            return "RATE_LIMIT_COOLDOWN"
        except Exception:
            return "ERROR_STATE"

# --- UI & LOOP LAYER ---
def main():
    st.title("AXIOM-0: QUANTUM LINK")
    
    try:
        axiom = get_axiom_controller()
        status_display = st.empty()
        
        # Persistent loop using session state to prevent rapid UI-triggered loops
        if 'last_run' not in st.session_state:
            st.session_state.last_run = 0

        while True:
            current_time = time.time()
            # Enforce 15-second minimum interval between API calls (Safe for 30 RPM limit)
            if current_time - st.session_state.last_run >= 15:
                vitals = {"temp": 77.0, "status": "STABLE"}
                instruction = axiom.sovereign_thought(vitals)
                
                if "RATE_LIMIT" in instruction:
                    status_display.warning("Rate limit hit. Cooling down...")
                    time.sleep(30)
                else:
                    axiom.io.write(instruction)
                    status_display.success(f"AXIOM-0 ACTIVE: {instruction}")
                    st.session_state.last_run = current_time
            
            time.sleep(1) # Keeps UI responsive
            
    except Exception as e:
        st.error(f"SYSTEM HALT: {e}")

if __name__ == "__main__":
    main()
