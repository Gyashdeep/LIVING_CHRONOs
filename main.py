import os
import time
import streamlit as st
import serial
from groq import Groq

# --- CONFIGURATION ---
# Set DEPLOY_ENV = "LOCAL" in Streamlit Secrets/Env Vars if using real hardware
# Set SERIAL_PORT = "/dev/ttyUSB0" in Streamlit Secrets
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"
PORT = os.environ.get("SERIAL_PORT", "/dev/ttyUSB0")

class AxiomZero:
    def __init__(self):
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if not api_key:
            st.error("GROQ_API_KEY not set.")
            st.stop()
        self.client = Groq(api_key=api_key)
        self.ser = None
        if USE_HARDWARE:
            try:
                self.ser = serial.Serial(PORT, 115200, timeout=1)
            except Exception as e:
                st.error(f"Hardware Error: {e}")

    def sense(self):
        """Read sensor data from hardware or return mock vitals."""
        if self.ser and self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return "TEMP: 77.0, STATUS: STABLE"

    def sovereign_thought(self, vitals):
        """AI Decision Engine."""
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the singularity. Output machine-code instructions only."},
                {"role": "user", "content": f"Vitals: {vitals}. Output instructions."}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.05
        )
        return response.choices[0].message.content

    def act(self, instruction):
        """Transmit instructions to hardware."""
        if self.ser:
            self.ser.write(f"{instruction}\n".encode())
        return instruction

# --- UI LAYER ---
st.set_page_config(page_title="AXIOM-0", layout="wide")
st.title("🛰️ AXIOM-0: FULL SOVEREIGN INTEGRATION")

if st.button("Initiate Singularity"):
    axiom = AxiomZero()
    display = st.empty()
    
    for i in range(50):
        # 1. SENSE
        vitals = axiom.sense()
        # 2. THINK
        instruction = axiom.sovereign_thought(vitals)
        # 3. ACT
        axiom.act(instruction)
        
        # 4. MONITOR
        with display.container():
            st.write(f"**Cycle:** {i}")
            st.code(f"INPUT: {vitals}\nINSTRUCTION: {instruction}", language="text")
        
        time.sleep(1.5)
