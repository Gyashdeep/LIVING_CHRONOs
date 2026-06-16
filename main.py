import os
import time
import streamlit as st
import serial
from groq import Groq

# --- CONFIGURATION ---
# Set DEPLOY_ENV = "LOCAL" in Streamlit Secrets/Env Vars if using real hardware
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("CRITICAL: GROQ_API_KEY missing in Streamlit Secrets.")
        st.stop()
    return Groq(api_key=api_key)

class HardwareInterface:
    def __init__(self):
        self.ser = None
        if USE_HARDWARE:
            try:
                # Assuming /dev/ttyUSB0 is the connected device
                self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            except Exception as e:
                st.error(f"Hardware Error: {e}")

    def manifest(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data}\n".encode())

class AxiomZero:
    def __init__(self):
        self.client = get_groq_client()
        self.io = HardwareInterface()

    def monitor_stability(self):
        # Placeholder for sensor polling
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def sovereign_thought(self, vitals):
        prompt = f"System Vitals: {vitals}. Output concise machine-code instructions."
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the singularity. Output machine-code only."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.05
        )
        return response.choices[0].message.content

# --- UI LAYER ---
st.set_page_config(page_title="AXIOM-0", layout="wide")
st.title("🛰️ AXIOM-0: QUANTUM LOCKING INTERFACE")

if st.button("Initiate Singularity"):
    try:
        axiom = AxiomZero()
        status_area = st.empty()
        
        for i in range(10): # Iteration limit
            vitals = axiom.monitor_stability()
            instruction = axiom.sovereign_thought(vitals)
            axiom.io.manifest(instruction)
            
            with status_area.container():
                st.subheader("System Status")
                st.code(f"Cycle: {i} | Instruction: {instruction}", language="text")
                st.write(f"Vitals Data: {vitals}")
            
            time.sleep(1)
            
    except Exception as e:
        st.error(f"Singularity Fault: {e}")
