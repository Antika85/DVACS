import re
from num2words import num2words
from tkinter import messagebox

def num2word_fun(language, file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        pattern = r'\b\d+\b'

        def replace_number(match):
            number = int(match.group(0))
            return num2words(number, lang=language)
        new_text = re.sub(pattern, replace_number, text)

        with open('text_num2word.txt', 'w', encoding='utf-8') as f:
            f.write(new_text)

        messagebox.showinfo('Успех',"Создан файл text_num2word.txt")

    except Exception as ex:
        messagebox.showerror("Ошибка", f"Произошла неизвестная ошибка, покажите её автору: {ex}")
