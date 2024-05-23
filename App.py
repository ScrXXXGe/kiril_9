import math
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GraphParams:
    def __init__(self, x_start, x_end, step_size, y_start):
        self.x_start = x_start
        self.x_end = x_end
        self.step_size = step_size
        self.y_start = y_start

def euler_method(x_start, y_start, x_end, step_size, func):
    x = np.arange(x_start, x_end, step_size)
    y = np.zeros(x.shape)
    y[0] = y_start
    for i in range(1, len(x)):
        y[i] = y[i-1] + step_size * func(x[i-1], y[i-1])
    return x, y

def differential_equation(x, y):
    return (math.sin(x) - y) * math.cos(x)

def plot_graph(params):
    x, y = euler_method(params.x_start, params.y_start, params.x_end, params.step_size, differential_equation)
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    ax.set_title('Graph')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    return fig

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotter")

        self.x_start = tk.StringVar(value="0.25")
        self.x_end = tk.StringVar(value="10.0")
        self.step_size = tk.StringVar(value="0.1")
        self.y_start = tk.StringVar(value="1.0")

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(input_frame, text="Start X").pack(pady=5)
        tk.Entry(input_frame, textvariable=self.x_start).pack(pady=5)

        tk.Label(input_frame, text="End X").pack(pady=5)
        tk.Entry(input_frame, textvariable=self.x_end).pack(pady=5)

        tk.Label(input_frame, text="Step size").pack(pady=5)
        tk.Entry(input_frame, textvariable=self.step_size).pack(pady=5)

        tk.Label(input_frame, text="Y Start").pack(pady=5)
        tk.Entry(input_frame, textvariable=self.y_start).pack(pady=5)

        tk.Button(input_frame, text="Recalculate", command=self.recalculate).pack(pady=20)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def recalculate(self):
        try:
            params = GraphParams(
                float(self.x_start.get()),
                float(self.x_end.get()),
                float(self.step_size.get()),
                float(self.y_start.get())
            )
            fig = plot_graph(params)
            self.display_graph(fig)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers.")

    def display_graph(self, fig):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
