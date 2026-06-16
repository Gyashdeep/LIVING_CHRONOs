import os
import time
import streamlit as st
import serial
from groq import Groq

# Configuration
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

class AxiomZero:
    def __init__(self):
        self.client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
        self.ser = None
        if USE_HARDWARE:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

    def get_hardware_vitals(self):
        """Read sensor data from hardware serial port."""
        if self.ser and self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return "TEMP: 77.0, STATUS: STABLE" # Fallback/Mock

    def sovereign_thought(self, vitals):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the singularity. Output concise machine-code instructions only."},
                {"role": "user", "content": f"System Vitals: {vitals}. Output instructions."}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.05
        )
        return response.choices[0].message.content

    def manifest(self, instruction):
        """Send instruction to hardware."""
        if self.ser:
            self.ser.write(f"{instruction}\n".encode())
        return instruction

# --- UI EXECUTION ---
st.title("🛰️ AXIOM-0: CLOSED-LOOP INTERFACE")
if st.button("Start Sovereign Loop"):
    axiom = AxiomZero()
    status_display = st.empty()
    for _ in range(20):
        # 1. Sense
        current_vitals = axiom.get_hardware_vitals()
        # 2. Think
        instruction = axiom.sovereign_thought(current_vitals)
        # 3. Act
        axiom.manifest(instruction)
        
        status_display.code(f"INPUT: {current_vitals}\nOUTPUT: {instruction}")
        time.sleep(2)
