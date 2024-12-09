import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def choose_file(title):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        return file_path
    else:
        messagebox.showerror('Ошибка:','Файл не был выбран!')
        return False

def choose_audiofile(title):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames(
        title=title,
        filetypes=[("Audio Files", ".wav .mp3"), ("All Files", "*.*")]
    )
    if file_path:
        return file_path
    else:
        messagebox.showerror('Ошибка:','Файл не был выбран!')
        return False

def choose_folder(title):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(
        title=title
    )
    if folder_path:
        return folder_path
    else:
        messagebox.showerror('Ошибка:','Папка не была выбрана!')
        return False
