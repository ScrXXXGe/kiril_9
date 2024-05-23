import tkinter as tk
from tkinter import messagebox

class EulerMethodODEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Euler Method ODE")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = EulerMethodODEApp()
    app.mainloop()
