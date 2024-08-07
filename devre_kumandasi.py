import tkinter as tk
from threading import Thread, Event
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
            button = tk.Button(self.button_frame, text=f"{btn.label}", width=25, command=lambda btn=btn: self.button_handler(btn))
            button.pack(pady=5)
            self.buttons.append(button)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def button_handler(self, btn):
        self.disable_buttons()

        event = Event()
        arduino_loop = Thread(target=arduino.run_loop, args=(btn, event))
        arduino_loop.daemon = True
        arduino_loop.start()

        self.root.after(100, lambda: self.check_thread_finished(event))

    def check_thread_finished(self, event):
        if event.is_set():
            self.enable_buttons()
        else:
            self.root.after(100, lambda: self.check_thread_finished(event))

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

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
