import os
import time
import streamlit as st
import serial
from groq import Groq

# --- CONFIGURATION ---
# Set DEPLOY_ENV = "LOCAL" in Streamlit Secrets or Environment Variables for hardware
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("CRITICAL: GROQ_API_KEY not found in Streamlit Secrets.")
        st.stop()
    return Groq(api_key=api_key)

class HardwareInterface:
    def __init__(self):
        self.ser = None
        if USE_HARDWARE:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            except Exception as e:
                st.error(f"Serial Hardware Unavailable: {e}")

    def manifest(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data}\n".encode())
        # Logic is handled by the UI display, so we don't print "Mock" here anymore

class AxiomZero:
    def __init__(self):
        self.client = get_groq_client()
        self.io = HardwareInterface()

    def monitor_stability(self):
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def sovereign_thought(self, vitals):
        prompt = f"System Vitals: {vitals}. Output concise machine-code instructions."
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the singularity. Output machine-code only."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-specdec",
            temperature=0.05
        )
        return response.choices[0].message.content

# --- MAIN APP EXECUTION ---
st.set_page_config(page_title="AXIOM-0", layout="wide")
st.title("🛰️ AXIOM-0: QUANTUM LOCKING INTERFACE")

if st.button("Initiate Singularity"):
    axiom = AxiomZero()
    status_display = st.empty()
    
    for i in range(20):
        vitals = axiom.monitor_stability()
        instruction = axiom.sovereign_thought(vitals)
        axiom.io.manifest(instruction)
        
        with status_display.container():
            st.metric("Cycle", i)
            st.subheader("Instruction Output:")
            st.code(instruction, language="text")
            st.write(f"System Vitals: {vitals}")
        
        time.sleep(1)
