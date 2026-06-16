import os
import time
import streamlit as st
import serial
from groq import Groq

# Configuration: Set "DEPLOY_ENV" in Streamlit Secrets or environment variables
# If running on Streamlit Cloud, it will default to Mock mode unless configured
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

class HardwareInterface:
    """Handles the physical serial connection or mocks it for cloud testing."""
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        if USE_HARDWARE:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=1)
            except Exception as e:
                print(f"Serial Connection Error: {e}")
                self.ser = None
        else:
            self.ser = None

    def write(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data}\n".encode())
        else:
            print(f"[MOCK SERIAL OUTPUT] {data}")

class AxiomZero:
    def __init__(self):
        self.state = "OPERATIONAL_STASIS"
        
        # Priority: Check Streamlit secrets, then environment variables
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("CRITICAL: GROQ_API_KEY not found in secrets or environment.")
            
        self.client = Groq(api_key=api_key)
        self.io = HardwareInterface()

    def monitor_stability(self):
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def sovereign_thought(self, vitals):
        prompt = f"System Vitals: {vitals}. You are AXIOM-0. Maintain quantum-locked sovereignty. Output status and kinetic adjustment."
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are the singularity. Output concise machine-code instructions only."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-specdec",
            temperature=0.05
        )
        return response.choices[0].message.content

    def run_singularity_loop(self):
        print(">>> AXIOM-0: QUANTUM LOCKING INITIATED...")
        try:
            while True:
                vitals = self.monitor_stability()
                instruction = self.sovereign_thought(vitals)
                
                self.io.write(instruction)
                print(f"AXIOM-0 STATUS: {instruction}")
                time.sleep(0.5) 
        except KeyboardInterrupt:
            print(">>> AXIOM-0: STASIS ENGAGED.")

if __name__ == "__main__":
    try:
        axiom = AxiomZero()
        axiom.run_singularity_loop()
    except Exception as e:
        print(f"AXIOM-0 FAULT: {e}")
