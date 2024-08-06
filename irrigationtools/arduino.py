import serial
import time
from enum import Enum


SERIAL_DEVICE           = "COM3"
SERIAL_PORT             = 9600
SECONDS_BEFORE_LOOP     = 5
MILISECONDS_BEFORE_LOOP = SECONDS_BEFORE_LOOP * 1000


class Button(Enum):
    AREA_1 = "Measure Area 1"
    AREA_2 = "Measure Area 2"
    AREA_3 = "Measure Area 3"
    AREA_4 = "Measure Area 4"
    AREA_5 = "Measure Area 5"

    def area_specific_delay(self, ms_format=False):
        delay = SECONDS_BEFORE_LOOP if not ms_format else MILISECONDS_BEFORE_LOOP

        match self:
            case self.AREA_1:
                delay += 5.1 if not ms_format else 5100
            case self.AREA_2:
                delay += 10.1 if not ms_format else 10100
            case self.AREA_3:
                delay += 15.1 if not ms_format else 15100
            case self.AREA_4:
                delay += 20.1 if not ms_format else 20100
            case self.AREA_5:
                delay += 25.1 if not ms_format else 25100

        return delay


class Signal(Enum):
    ON = "on"
    OFF = "off"


class Arduino:
    def __init__(self, device=SERIAL_DEVICE, baudrate=SERIAL_PORT):
        self.device = device
        self.baudrate = baudrate
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.device, self.baudrate, timeout=1)
            print(f"Connected to {self.device} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting: {e}")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.emit(Signal.OFF, output=False)
            self.ser.close()
            print("Disconnected from Arduino.")

    def emit(self, signal, output=True):
        if not isinstance(signal, Signal):
            raise ValueError("Recieved unknown signal")

        if self.ser and self.ser.is_open:
            self.ser.write(bytes(signal.value, "utf-8"))
            response = self.ser.readline().decode("utf-8").strip()
            if output:
                print("ARDUINO:", response)
        else:
            print("Not connected to Arduino.")
            return None

    def run_loop(self, btn):
        delay = btn.area_specific_delay()

        time.sleep(SECONDS_BEFORE_LOOP)
        self.emit(Signal.ON)
        time.sleep(delay)
        self.emit(Signal.OFF)
