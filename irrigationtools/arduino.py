import serial
import time
from enum import Enum
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

SERIAL_DEVICE           = "COM6"
SERIAL_PORT             = 9600
SECONDS_BEFORE_LOOP     = 5
MILISECONDS_BEFORE_LOOP = SECONDS_BEFORE_LOOP * 1000
MOISTURE_SENSOR_MIN     = 120
MOISTURE_SENSOR_MAX     = 800


class Button(Enum):
    AREA_1 = ("Nem Ölç Bölge 1", 0)
    AREA_2 = ("Nem Ölç Bölge 2", 1)
    AREA_3 = ("Nem Ölç Bölge 3", 2)
    AREA_4 = ("Nem Ölç Bölge 4", 3)

    def __init__(self, label, relay_index):
        self.label       = label
        self.relay_index = relay_index


class Signal(Enum):
    ON            = "on"
    OFF           = "off"
    READ_MOISTURE = "read_moisture"


class Arduino:
    def __init__(self, device=SERIAL_DEVICE, baudrate=SERIAL_PORT):
        self.device   = device
        self.baudrate = baudrate
        self.ser      = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.device, self.baudrate, timeout=1)
            print(f"Connected to {self.device} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting: {e}")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            print("Disconnecting from Arduino...")
            
            for btn in Button:
                self.emit(Signal.OFF, btn.relay_index, output=False)
                time.sleep(0.1)
            self.ser.close()
            
            print("Disconnected.")

    def emit(self, signal, relay_index=None, output=True):
        if not isinstance(signal, Signal):
            raise ValueError("Received unknown signal")

        if self.ser and self.ser.is_open:
            if relay_index is not None:
                command = f"{signal.value}{relay_index}"
            else:
                command = signal.value
                
            self.ser.write(bytes(command, "utf-8"))
            response = self.ser.readline().decode("utf-8").strip()
            
            if output:
                print("ARDUINO:", response)
            else:
                return response
        else:
            print("Not connected to Arduino.")
            return None

    def run_loop(self, btn, event):
        time.sleep(SECONDS_BEFORE_LOOP)

        moisture = self.get_moisture(btn.relay_index)
        if moisture is None:
            return

        print("=> Sensor nem:", moisture)

        delay = int(self.scale_value(moisture, new_min=2, new_max=10))

        print(f"=> Vanalarin calisma suresi {delay} saniye olarak belirlendi.")

        time.sleep(SECONDS_BEFORE_LOOP)

        self.emit(Signal.ON, btn.relay_index)
        time.sleep(delay)
        self.emit(Signal.OFF, btn.relay_index)

        event.set()

    def get_moisture(self, area):
        moisture = self.emit(Signal.READ_MOISTURE, output=False)
        warning = "WARNING: Something went wrong with reading moisture value"

        if not moisture or not moisture.isnumeric():
            print(warning)
            return None

        try:
            moisture = int(moisture)
        except ValueError:
            print(warning)
            return None
        
        self.save_to_dashboard(moisture, area)
        
        return moisture
    
    def save_to_dashboard(self, moisture, area):
        match (area):
            case 0:
                api_url = os.getenv("API_URL_A")
            case 1:
                api_url = os.getenv("API_URL_B")
            case 2:
                api_url = os.getenv("API_URL_C")
            case 3:
                api_url = os.getenv("API_URL_D")
            case _:
                print("ERROR: Something is wrong with saving to dashboard.")
                return
                
        moisture_percent = ((MOISTURE_SENSOR_MAX - moisture) / (MOISTURE_SENSOR_MAX-MOISTURE_SENSOR_MIN)) * 100

        curl = [
            "curl", "-v", "-X", "POST", api_url,
            "--header", "Content-Type:application/json",
            "--data", f'{{"moisture": {moisture_percent}}}'
        ]
        
        subprocess.run(curl, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @staticmethod
    def scale_value(value, new_min, new_max, old_min=MOISTURE_SENSOR_MIN, old_max=MOISTURE_SENSOR_MAX):
        old_range = old_max - old_min
        new_range = new_max - new_min
        scaled_value = (((value - old_min) * new_range) / old_range) + new_min
        return scaled_value
