import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        
        self.running = False
        
        # Time Interval Frame
        interval_frame = ttk.LabelFrame(root, text="Click Interval")
        interval_frame.pack(padx=10, pady=5)

        self.hours = tk.IntVar(value=0)
        self.minutes = tk.IntVar(value=0)
        self.seconds = tk.IntVar(value=0)
        self.milliseconds = tk.IntVar(value=100)
        
        ttk.Entry(interval_frame, textvariable=self.hours, width=7).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(interval_frame, text="hours").grid(row=0, column=1, padx=5, pady=5)
        ttk.Entry(interval_frame, textvariable=self.minutes, width=7).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(interval_frame, text="mins").grid(row=0, column=4, padx=5, pady=5)
        ttk.Entry(interval_frame, textvariable=self.seconds, width=7).grid(row=0, column=5, padx=5, pady=5)
        ttk.Label(interval_frame, text="secs").grid(row=0, column=6, padx=5, pady=5)
        ttk.Entry(interval_frame, textvariable=self.milliseconds, width=5).grid(row=0, column=7, padx=5, pady=5)
        ttk.Label(interval_frame, text="milliseconds").grid(row=0, column=8, padx=5, pady=5)
        
        # Cursor Position Frame
        position_frame = ttk.LabelFrame(root, text="Cursor Position")
        position_frame.pack(padx=10, pady=5)
        
        # position_current_frame = ttk.Frame(position_frame)
        # position_current_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # position_specific_frame = ttk.Frame(position_frame)
        # position_specific_frame.grid(row=0, column=1, padx=5, pady=5)
        
        self.use_current_position = tk.BooleanVar(value=True)
        # ttk.Radiobutton(position_current_frame, text="Current Position", variable=self.use_current_position, value=True).pack(anchor=tk.W, padx=5, pady=5)
        
        # ttk.Radiobutton(position_specific_frame, text="Pick Location:", variable=self.use_current_position, value=False).pack(anchor=tk.W, padx=5, pady=5)

        ttk.Radiobutton(position_frame, text="Current Position", variable=self.use_current_position, value=True).grid(row=0, column=0, padx=45, pady=5)
        
        ttk.Radiobutton(position_frame, text="Pick Location:", variable=self.use_current_position, value=False).grid(row=0, column=1, padx=5, pady=5)
        
        self.x_position = tk.IntVar(value=0)
        self.y_position = tk.IntVar(value=0)
        
        # ttk.Entry(position_specific_frame, textvariable=self.x_position, width=5).pack(side=tk.LEFT, padx=5, pady=5)
        # ttk.Label(position_specific_frame, text="X").pack(side=tk.LEFT, padx=5, pady=5)
        # ttk.Entry(position_specific_frame, textvariable=self.y_position, width=5).pack(side=tk.LEFT, padx=5, pady=5)
        # ttk.Label(position_specific_frame, text="Y").pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(position_frame, text="X").grid(row=0, column=2, padx=0, pady=5)
        ttk.Entry(position_frame, textvariable=self.x_position, width=5).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(position_frame, text="Y").grid(row=0, column=4, padx=0, pady=5)
        ttk.Entry(position_frame, textvariable=self.y_position, width=5).grid(row=0, column=5, padx=5, pady=5)
        
        # Start and Stop Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)
        
        self.start_button = ttk.Button(button_frame, text="Start (F6)", command=self.start_clicking)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.BOTH)
        
        self.stop_button = ttk.Button(button_frame, text="Stop (F6)", command=self.stop_clicking)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.BOTH)
        
        # Creator Text
        creator_label = ttk.Label(root, text="Created by lyudmilov-georgedi", anchor="e")
        creator_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Key Listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
    def start_clicking(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.running = True
        self.click_thread = threading.Thread(target=self.click)
        self.click_thread.start()
        
    def stop_clicking(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.running = False
        if self.click_thread.is_alive():
            self.click_thread.join()
    
    def click(self):
        interval = (self.hours.get() * 3600 + self.minutes.get() * 60 + self.seconds.get() + self.milliseconds.get() / 1000)
        while self.running:
            if self.use_current_position.get():
                pyautogui.click()
            else:
                pyautogui.click(x=self.x_position.get(), y=self.y_position.get())
            time.sleep(interval)
        
    def on_press(self, key):
        if key == keyboard.Key.f6:
            if self.running:
                self.stop_clicking()
            else:
                self.start_clicking()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
