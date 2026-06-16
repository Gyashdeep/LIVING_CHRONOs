import os
import time
import json
import serial
from groq import Groq, BadRequestError

# Configuration
USE_HARDWARE = os.environ.get("DEPLOY_ENV") == "LOCAL"

class HardwareInterface:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.ser = None
        if USE_HARDWARE:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=1)
            except Exception as e:
                print(f"Hardware connection failed: {e}")

    def write(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data.strip()}\n".encode())
        else:
            print(f"[MOCK SERIAL OUTPUT] {data.strip()}")

class AxiomZero:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.io = HardwareInterface()
        # Use a verified production-ready model
        self.model = "llama-3.3-70b-versatile" 

    def monitor_stability(self):
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def sovereign_thought(self, vitals):
        # Ensure input is a string/JSON
        prompt = f"System Vitals: {json.dumps(vitals)}. Output concise machine-code instructions only."
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AXIOM-0. Maintain sovereignty."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.05
            )
            return response.choices[0].message.content
        except BadRequestError as e:
            # This captures the specific API error details
            print(f"Groq API Bad Request: {e.response.json()}")
            return "ERROR: INVALID_MODEL_OR_PAYLOAD"
        except Exception as e:
            print(f"General Error: {e}")
            return "ERROR: SYSTEM_EXCEPTION"

    def run_singularity_loop(self):
        print(">>> AXIOM-0: INITIALIZING...")
        while True:
            try:
                vitals = self.monitor_stability()
                instruction = self.sovereign_thought(vitals)
                self.io.write(instruction)
                print(f"AXIOM-0 STATUS: {instruction}")
                time.sleep(2) # Increased sleep to prevent rate limiting
            except KeyboardInterrupt:
                print(">>> AXIOM-0: STASIS ENGAGED.")
                break

if __name__ == "__main__":
    axiom = AxiomZero()
    axiom.run_singularity_loop()
