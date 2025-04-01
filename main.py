import time
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StockSimulation:
    def __init__(self, root):
        self.running = False
        self.speed = 1.0  # 1x speed
        self.stocks = {"AAPL": 150.0, "GOOGL": 2800.0, "AMZN": 3500.0}
        self.history = {stock: [] for stock in self.stocks}
        self.events = ["Market Crash", "NOICE", "Regulatory Changes"]
        
        self.root = root
        self.root.title("Stock Simulator")
        
        self.stock_labels = {}
        for stock in self.stocks:
            label = ttk.Label(root, text=f"{stock}: {self.stocks[stock]:.2f}")
            label.pack()
            self.stock_labels[stock] = label
        
        self.event_label = ttk.Label(root, text="Events: None")
        self.event_label.pack()
        
        self.speed_scale = ttk.Scale(root, from_=0.1, to=5.0, orient=tk.HORIZONTAL, command=self.update_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()
        
        self.start_button = ttk.Button(root, text="Start", command=self.start)
        self.start_button.pack()
        
        self.pause_button = ttk.Button(root, text="Pause", command=self.pause)
        self.pause_button.pack()
        
        self.resume_button = ttk.Button(root, text="Resume", command=self.resume)
        self.resume_button.pack()
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()
    
    def start(self):
        self.running = True
        self.run_simulation()
    
    def run_simulation(self):
        if self.running:
            self.update_market()
            self.update_graph()
            self.root.after(int(1000 / self.speed), self.run_simulation)
    
    def update_market(self):
        for stock in self.stocks:
            self.stocks[stock] += random.uniform(-5, 5)
            self.stock_labels[stock].config(text=f"{stock}: {self.stocks[stock]:.2f}")
            self.history[stock].append(self.stocks[stock])
        if random.random() < 0.1:
            self.trigger_event()
    
    def trigger_event(self):
        event = random.choice(self.events)
        self.event_label.config(text=f"Event triggered: {event}")
        if event == "Market Crash":
            for stock in self.stocks:
                self.stocks[stock] *= 0.8
        elif event == "Booming Economy":
            for stock in self.stocks:
                self.stocks[stock] *= 1.2
    
    def update_graph(self):
        self.ax.clear()
        for stock, prices in self.history.items():
            self.ax.plot(prices, label=stock)
        self.ax.legend()
        self.canvas.draw()
    
    def update_speed(self, val):
        self.speed = float(val)
    
    def pause(self):
        self.running = False
    
    def resume(self):
        self.running = True
        self.run_simulation()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockSimulation(root)
    root.mainloop()
