import serial
import time
from enum import Enum


SERIAL_DEVICE           = "COM3"
SERIAL_PORT             = 9600
SECONDS_BEFORE_LOOP     = 5
MILISECONDS_BEFORE_LOOP = SECONDS_BEFORE_LOOP * 1000
MOISTURE_SENSOR_MIN     = 0
MOISTURE_SENSOR_MAX     = 1023


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
                time.sleep(0.5)
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

        moisture = self.get_moisture()
        if moisture is None:
            return

        print("=> Sensor nem:", moisture)

        delay = int(self.scale_value(moisture, new_min=5, new_max=20))

        print(f"=> Vanalarin calisma suresi {delay} saniye olarak belirlendi.")

        time.sleep(SECONDS_BEFORE_LOOP)

        self.emit(Signal.ON, btn.relay_index)
        time.sleep(delay)
        self.emit(Signal.OFF, btn.relay_index)

        event.set()

    def get_moisture(self):
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

        return moisture

    @staticmethod
    def scale_value(value, new_min, new_max, old_min=MOISTURE_SENSOR_MIN, old_max=MOISTURE_SENSOR_MAX):
        old_range = old_max - old_min
        new_range = new_max - new_min
        scaled_value = (((value - old_min) * new_range) / old_range) + new_min
        return scaled_value
