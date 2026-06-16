import os
import time
import json
import streamlit as st
from groq import Groq, RateLimitError

# --- HARDWARE INTERFACE ---
class HardwareInterface:
    def __init__(self):
        self.use_hardware = os.environ.get("DEPLOY_ENV") == "LOCAL"
        self.ser = None
        if self.use_hardware:
            try:
                import serial
                self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            except Exception as e:
                st.error(f"Hardware init failed: {e}")

    def write(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data.strip()}\n".encode())
        else:
            st.write(f" [MOCK SERIAL] >> {data.strip()}")

# --- CORE LOGIC ---
class AxiomZero:
    def __init__(self):
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in secrets.")
        self.client = Groq(api_key=api_key)
        self.io = HardwareInterface()

    def monitor_stability(self):
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def sovereign_thought(self, vitals):
        prompt = f"System Vitals: {json.dumps(vitals)}. Output status and kinetic adjustment."
        
        # Exponential backoff for Rate Limits
        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are AXIOM-0. Output machine-code instructions only."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.05
                )
                return response.choices[0].message.content
            
            except RateLimitError:
                wait_time = (2 ** attempt) + 2 
                st.warning(f"Rate limit reached. Waiting {wait_time}s...")
                time.sleep(wait_time)
            except Exception as e:
                st.error(f"API Error: {e}")
                break
        return "ERROR: COMPUTE_STASIS"

    def run_singularity_loop(self):
        st.write("### AXIOM-0: QUANTUM LOCKING INITIATED...")
        status_area = st.empty()
        
        while True:
            vitals = self.monitor_stability()
            instruction = self.sovereign_thought(vitals)
            
            self.io.write(instruction)
            status_area.write(f"**AXIOM-0 Status:** {instruction}")
            
            # Increased sleep to maintain < 30 RPM (Groq's limit)
            time.sleep(3) 

# --- EXECUTION ---
if __name__ == "__main__":
    try:
        axiom = AxiomZero()
        axiom.run_singularity_loop()
    except Exception as e:
        st.error(f"SYSTEM FAILURE: {e}")
