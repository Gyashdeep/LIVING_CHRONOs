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
                print(f"Failed to connect to hardware: {e}")

    def write(self, data: str):
        if self.ser:
            self.ser.write(f"CMD:{data.strip()}\n".encode())
        else:
            print(f"[MOCK SERIAL OUTPUT] {data.strip()}")

class AxiomZero:
    def __init__(self):
        self.state = "OPERATIONAL_STASIS"
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.io = HardwareInterface()
        # Use a verified model name
        self.model = "llama-3.3-70b-versatile" 

    def monitor_stability(self):
        return {"temp": 77.0, "flux_pinning": "STABLE"}

    def sovereign_thought(self, vitals):
        prompt = f"System Vitals: {json.dumps(vitals)}. Output status and kinetic adjustment."
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AXIOM-0. Output concise machine-code instructions only."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.05
            )
            return response.choices[0].message.content
        except BadRequestError as e:
            # This will print the actual error from Groq in your logs
            print(f"Groq API Error: {e.response.json()}")
            return "ERROR: INVALID_INSTRUCTION"
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return "ERROR: SYSTEM_FAILURE"

    def run_singularity_loop(self):
        print(">>> AXIOM-0: QUANTUM LOCKING INITIATED...")
        while True:
            try:
                vitals = self.monitor_stability()
                instruction = self.sovereign_thought(vitals)
                self.io.write(instruction)
                print(f"AXIOM-0 STATUS: {instruction}")
                time.sleep(0.5) 
            except KeyboardInterrupt:
                print(">>> AXIOM-0: STASIS ENGAGED.")
                break

if __name__ == "__main__":
    axiom = AxiomZero()
    axiom.run_singularity_loop()
