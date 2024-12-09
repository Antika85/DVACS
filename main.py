import os
from doctest import master

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import time
import threading

from choose_explorer import choose_file, choose_audiofile, choose_folder

from count_fragment import count_fragment_fun
from num2word import num2word_fun

from break_time import break_time_fun
from topmedia2 import topmedia2_fun

from audioredactor2 import process_files_in_parallel
from subcreator import subcreator_fun


def count_fragment_start():
    file = choose_file('Выберите текстовый файл (.txt) - Программа выведет количество абзацев в файле')
    if file != False:
        count_fragment_fun(str(file))

def num2word_start():
    file = choose_file('Выберите текстовый файл (.txt) - Все цифры в файле будут заменены на словесный вид')
    if file != False:
        language = language_menu.get()[-2:]
        print(language)
        num2word_fun(language, str(file))

def break_time_start():
    file = choose_file('Выберите текстовый файл (.txt) - По тексту из файла будут созданы текстовые документы с паузами по 5 секунд (для TopMedia)')
    if file != False:
        break_time_fun(str(file))

def topmedia2_start():
    files = choose_audiofile('Выберите ВСЕ аудиофайлы, которые вы скачали из TopMedia')
    if files != False:
        threading.Thread(target=topmedia2_fun,
                         args=(files,),
                         daemon=True).start()

def audioredactor2_start():
    silence_threshold = int(silence_threshold_entry.get())
    audio_extension = extensions_menu.get()
    input_folder = choose_folder('Выберите папку с аудиофайлами - Из них будут вырезаны пустоты')
    if input_folder != False:
        if audio_extension == '.mp3':
            messagebox.showinfo("Внимание!", "При использовании mp3 у вас будут открываться и закрываться консольные окна от ffmpeg. Ничего страшного в этом нет!")
        threading.Thread(target=process_files_in_parallel,
                         args=(silence_threshold, audio_extension, input_folder),
                         daemon=True).start()

def subcreator_start():
    file = choose_file('Выберите текстовый файл (.txt) - Субтитры будут созданы по тексту из файла')
    if file != False:
        folder = choose_folder('Выберите папку с аудиофайлами - Для них будут созданы субтитры')
        if folder != False:
            fps = int(fps_entry.get())
            audio_extension = extensions_menu.get()
            subs = subs_checkbox.get()
            subcreator_fun(fps, audio_extension, str(file), str(folder), subs)


def topmedia_start_all_process_silence(files,file):
    # Удаление пауз в 5 секунд
    topmedia2_fun(files)

    # Удаление пустот
    silence_threshold = 500
    audio_extension = 'wav'
    input_folder = 'audiofiles_from_topmedia'
    process_files_in_parallel(silence_threshold, audio_extension, input_folder)

    # Создание сабов
    fps = 30
    audio_extension = 'wav'
    folder = 'result'
    subs = True
    subcreator_fun(fps, audio_extension, str(file), folder, subs)

def topmedia_start_all_processes():
    files = choose_audiofile('Выберите ВСЕ аудиофайлы, которые вы скачали из TopMedia')
    file = choose_file('Выберите текстовый файл (.txt) - Субтитры будут созданы по тексту из файла')
    if files != False and file != False:
        threading.Thread(target=topmedia_start_all_process_silence,
                         args=(files,file),
                         daemon=True).start()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("DVACS")
    root.resizable(width=False,height=False)

    tabview = ctk.CTkTabview(master=root)
    tabview.pack(padx=20, pady=20)

    tabview.add("PlatHT")
    tabview.add("TopMedia")
    tabview.add("Админ-Панель")
    tabview.set("TopMedia")

    frame_topmedia = tabview.tab('TopMedia')
    frame_admin = tabview.tab('Админ-Панель')

    # TopMedia панель для быстрого и простого доступа
    ctk.CTkLabel(master=frame_topmedia, wraplength=500, justify='left', text='Простая инструкция по созданию озвучки и шаблона субтитр через TopMedia').pack()
    ctk.CTkLabel(master=frame_topmedia, wraplength=500, justify='left', text='1. Создайте текстовый файл (.txt) и вставьте в него текст вашего видео').pack(anchor='w')
    ctk.CTkLabel(master=frame_topmedia, wraplength=500, justify='left', text='2. Нажмите на кнопку ниже и выберите созданный текстовый файл (.txt). Будут созданы от 1 до 20 текстовых документов (.docx)').pack(anchor='w')
    ctk.CTkButton(frame_topmedia, text='Создать текстовый(ые) документ(ы)', command=break_time_start).pack(anchor='w', pady=[0,15])
    ctk.CTkLabel(master=frame_topmedia, wraplength=500, justify='left', text='3. Используя текстовые документы сгенерируйте аудиофайлы через TopMedia. Скачайте их и пронумеруйте (1-2-3 и т.д.)\n').pack(anchor='w')
    ctk.CTkLabel(master=frame_topmedia, wraplength=500, justify='left', text='4. Нажмите на кнопку ниже. Выберите сгенерированные аудиофайлы и изначальный текстовый файл (.txt). Будут созданы: папка с готовыми аудиофайлами, два файла с субтитрами (.srt)').pack(anchor='w')
    ctk.CTkButton(frame_topmedia, text='Редактировать аудиофайлы и создать субтитры', command=topmedia_start_all_processes).pack(anchor='w', pady=[0,15])

    # Админская панель со всеми возможностями
    count_fragmet_button = ctk.CTkButton(master=frame_admin, text='Узнать количество абзацев в тексте', command=count_fragment_start)
    count_fragmet_button.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)

    languages_num2word = ["Английский: en", "Русский: ru", "Испанский: es", "Французский: fr", "Немецкий: de",
                          "Итальянский: it", "Португальский: pt", "Нидерландский: nl", "Турецкий: tr", "Польский: pl",
                          "Литовский: lt", "Латышский: lv", "Болгарский: bg", "Чешский: cs", "Словенский: sl",
                          "Венгерский: hu", "Греческий: el", "Румынский: ro", "Индонезийский: id", "Арабский: ar",
                          "Шведский: sv", "Финский: fi", "Украинский: uk", "Вьетнамский: vi", "Иврит: he"]

    language_menu = ctk.CTkOptionMenu(master=frame_admin, values=languages_num2word)
    language_menu.grid(row=1, column=0, columnspan=1, sticky='ew', pady=5)

    count_fragmet_button = ctk.CTkButton(frame_admin, text='Заменить цифры на слова',command=num2word_start)
    count_fragmet_button.grid(row=1, column=1, columnspan=1, sticky='ew', pady=5)

    break_time_button = ctk.CTkButton(frame_admin, text='Вставить паузы 5с', command=break_time_start)
    break_time_button.grid(row=2, column=0, columnspan=2, sticky='ew', pady=[5,0])

    topmedia2_button = ctk.CTkButton(master=frame_admin, text='Разделить аудио из TopMedia', command=topmedia2_start)
    topmedia2_button.grid(row=3, column=0, columnspan=2, sticky='ew', pady=[0,15])

    frame_1 = ctk.CTkFrame(master=frame_admin)
    frame_1.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)

    ctk.CTkLabel(master=frame_1, text='Исходное расширение:').grid(row=0, column=0, columnspan=1, sticky='ew')
    ctk.CTkLabel(master=frame_1, text='Значение тишины:').grid(row=0, column=1, columnspan=1, sticky='ew')

    audio_extensions = ['wav', 'mp3']
    extensions_menu = ctk.CTkOptionMenu(master=frame_1, values=audio_extensions,width=80)
    extensions_menu.grid(row=1, column=0, columnspan=1, sticky='ew')

    silence_threshold_entry = ctk.CTkEntry(master=frame_1)
    silence_threshold_entry.insert(0, "500")
    silence_threshold_entry.grid(row=1, column=1, columnspan=1, sticky='ew')

    process_button = ctk.CTkButton(frame_1, text="Вырезать тишину и паузы", command=audioredactor2_start)
    process_button.grid(row=1, column=3, columnspan=1, sticky='ew')

    frame_2 = ctk.CTkFrame(master=frame_admin)
    frame_2.grid(row=6, column=0, columnspan=2, sticky='ew')

    ctk.CTkLabel(frame_2, text="FPS проекта:").grid(row=0, column=1, columnspan=1, sticky='ew', pady=[5,0])

    checkbox_value = ctk.BooleanVar()
    subs_checkbox = ctk.CTkCheckBox(frame_2, text='Аудио по предложениям?', font=('Arial',12), variable=checkbox_value)
    subs_checkbox.grid(row=1, column=0, columnspan=1, sticky='ew', padx=[0,5])

    fps_entry = ctk.CTkEntry(frame_2)
    fps_entry.insert(0, "30")
    fps_entry.grid(row=1, column=1, columnspan=1, sticky='ew')

    subtitle_button = ctk.CTkButton(frame_2, text="Создать субтитры", command=subcreator_start)
    subtitle_button.grid(row=1, column=2, columnspan=1, sticky='ew')

    root.mainloop()