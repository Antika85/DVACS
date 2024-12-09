from tkinter import messagebox

def count_fragment_fun(file):
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()
            paragraphs = [p.strip() for p in content.splitlines() if p.strip()]
            messagebox.showinfo("Успех!",f"Количество абзацев в тексте: {len(paragraphs)}")
    except Exception as ex:
        messagebox.showerror("Ошибка", f"Произошла неизвестная ошибка, покажите её автору: {ex}")


