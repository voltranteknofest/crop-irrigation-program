import tkinter as tk
from threading import Thread
from irrigationtools.arduino import Arduino, Button


WINDOW_TITLE = "Remote"
WINDOW_GEOMETRY = "300x300"


class CircuitGui:
    def __init__(self, root, arduino):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(expand=True)

        self.buttons = []
        for btn in Button:
            button = tk.Button(self.button_frame, text=f"{btn.value}", width=25, command=lambda btn=btn: self.button_handler(btn))
            button.pack(pady=5)
            self.buttons.append(button)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def button_handler(self, btn):
        delay = btn.area_specific_delay(ms_format=True)
        delay += 7000 # additional time to cover up arduino's latency
                
        self.disable_buttons(delay)
        
        arduino_loop = Thread(target=arduino.run_loop, args=(btn,))
        arduino_loop.daemon = True
        arduino_loop.start()

    def disable_buttons(self, time):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.root.after(time, self.enable_buttons)

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def on_close(self):
        arduino.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    arduino = Arduino()
    arduino.connect()
    
    root = tk.Tk()
    app = CircuitGui(root, arduino)
    root.mainloop()
