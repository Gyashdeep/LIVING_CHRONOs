import os
import time
import streamlit as st
import serial
from groq import Groq

# 1. Configuration: Streamlit handles secrets securely
# Ensure you have [secrets] in your Dashboard -> Settings -> Secrets
def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.environ.get("GROQ_API_KEY")

class HardwareInterface:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        # We use a flag to prevent trying to open physical ports in the cloud
        self.use_hardware = os.environ.get("DEPLOY_ENV") == "LOCAL"
        self.ser = None
        if self.use_hardware:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=1)
            except Exception as e:
                st.error(f"Serial Error: {e}")

    def write(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data}\n".encode())
        else:
            st.write(f"MOCK OUTPUT: {data}")

class AxiomZero:
    def __init__(self):
        api_key = get_api_key()
        if not api_key:
            st.error("CRITICAL: GROQ_API_KEY is missing.")
            st.stop() # Prevents further execution
        self.client = Groq(api_key=api_key)
        self.io = HardwareInterface()

    def monitor_stability(self):
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def run_singularity_loop(self):
        st.title("AXIOM-0 Singularity Interface")
        placeholder = st.empty()
        
        # Loop for a fixed number of iterations so the app doesn't hang forever
        for _ in range(50):
            vitals = self.monitor_stability()
            # ... (your logic here)
            instruction = "STASIS_MAINTAINED"
            self.io.write(instruction)
            
            with placeholder.container():
                st.write(f"Status: {instruction}")
            
            time.sleep(1)

# Ensure this is the ONLY entry point
if __name__ == "__main__":
    axiom = AxiomZero()
    axiom.run_singularity_loop()
