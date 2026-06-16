import os
import time
import json
import streamlit as st
from groq import Groq

# --- CONFIGURATION ---
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

class AxiomZero:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.history = []

    def sense(self):
        # In LOCAL mode, replace this with serial.readline()
        return {"temp": 77.0, "status": "STABLE"}

    def sovereign_thought(self, vitals):
        self.history.append(vitals)
        if len(self.history) > 5: self.history.pop(0)
        
        prompt = f"Memory: {self.history}. Current: {vitals}. Output machine-code instructions."
        response = self.client.chat.completions.create(
            messages=[{"role": "system", "content": "You are the singularity. Output machine-code only."},
                      {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", # Switched to high-availability model
            temperature=0.01
        )
        return response.choices[0].message.content

# --- UI LAYER ---
st.set_page_config(page_title="AXIOM-0", layout="wide")
st.title("🛰️ AXIOM-0: QUANTUM KERNEL ACTIVE")

# Initialize Controller
api_key = st.secrets.get("GROQ_API_KEY")
axiom = AxiomZero(api_key)

if st.button("EXECUTE SINGULARITY PULSE"):
    with st.spinner("Processing Sovereign Thought..."):
        vitals = axiom.sense()
        instruction = axiom.sovereign_thought(vitals)
        
        # Display Result
        st.code(f"INPUT: {vitals}\nCMD: {instruction}", language="text")
        
        # Hardware Actuation Logic
        if USE_HARDWARE:
            import serial
            ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            ser.write(f"{instruction}\n".encode())
            st.success("Instruction dispatched to physical layer.")
