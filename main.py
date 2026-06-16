import os
import time
import serial
from groq import Groq

# Configuration: Set "LOCAL" in your environment variables to enable real serial
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

class HardwareInterface:
    """Handles the physical serial connection or mocks it for cloud testing."""
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        if USE_HARDWARE:
            self.ser = serial.Serial(port, baudrate, timeout=1)
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
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.io = HardwareInterface()

    def monitor_stability(self):
        # In production, replace with actual sensor polling logic
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
        while True:
            try:
                vitals = self.monitor_stability()
                instruction = self.sovereign_thought(vitals)
                
                # Manifest: Signal the physical hardware or mock
                self.io.write(instruction)
                
                print(f"AXIOM-0 STATUS: {instruction}")
                time.sleep(0.5) 
            except KeyboardInterrupt:
                print(">>> AXIOM-0: STASIS ENGAGED.")
                break

if __name__ == "__main__":
    axiom = AxiomZero()
    axiom.run_singularity_loop()
