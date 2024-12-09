import tkinter as tk
from tkinter import ttk

class ProgressBar:
    def __init__(self, max_value, name_process, message=''):
        self.process_window = tk.Toplevel()
        self.process_window.title("Окно процесса")
        self.process_window.geometry("500x150")

        self.max_value = max_value
        self.name_process = name_process
        self.progress_label = tk.Label(self.process_window, text=f'{self.name_process}: 0% (0/{max_value})')
        self.progress_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.process_window, length=300, mode='determinate', maximum=self.max_value)
        self.progress.pack(pady=5)

        self.message = message
        self.message_label = tk.Label(self.process_window)
        self.message_label.pack(pady=5)

    def update_progress(self, current_value):
        self.progress['value'] = current_value
        current_percent = int(current_value / self.max_value * 100)
        self.progress_label.config(text=f"{self.name_process}: {current_percent}% ({current_value}/{self.max_value})")

    def message_fun(self, message):
        self.message = message
        self.message_label.config(text=message)



