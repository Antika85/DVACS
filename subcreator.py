import os
import re
from pydub import AudioSegment
from tkinter import messagebox
from paragraps_and_sentences_script import fun_find_paragraphs_and_sentences

from progress_bar_script import ProgressBar

def format_time(hours, minutes, seconds, milliseconds):
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

def calculate_next_time(start_time, duration_ms):
    hours, minutes, seconds, milliseconds = start_time

    total_milliseconds = milliseconds + duration_ms
    total_seconds = seconds + total_milliseconds // 1000
    total_milliseconds %= 1000
    total_minutes = minutes + total_seconds // 60
    total_seconds %= 60
    total_hours = hours + total_minutes // 60
    total_minutes %= 60

    return total_hours, total_minutes, total_seconds, total_milliseconds

def extract_index(filename):
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else float('inf')

def round_time_to_frame(time, frame_duration):
    hours, minutes, seconds, milliseconds = time
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    total_ms = int(total_ms // frame_duration * frame_duration)

    new_hours = total_ms // 3600000
    total_ms %= 3600000
    new_minutes = total_ms // 60000
    total_ms %= 60000
    new_seconds = total_ms // 1000
    new_milliseconds = total_ms % 1000

    return new_hours, new_minutes, new_seconds, new_milliseconds

def subcreator_fun(fps, audio_extension, file, input_folder, subs):
    print(subs)
    start_time = (0, 0, 0, 0)

    if subs:
        paragraphs_and_sentences, phrase = fun_find_paragraphs_and_sentences(file)
    else:
        with open(file,'r',encoding='utf-8') as f:
            content = f.read().strip()
            phrase = [p.strip() for p in content.splitlines() if p.strip()]

    audio_files = sorted([f for f in os.listdir(input_folder) if f.endswith(f'.{audio_extension}')],key=extract_index)
    count_files = len(audio_files)
    counf_phrase = len(phrase)

    progress_bar = ProgressBar(max_value=count_files, name_process='Создание субтитров')

    ends = []
    with open('sub.srt', 'w', encoding='utf-8') as sub_file:
        frame_duration = 1000 / fps
        for index in range(count_files):
            file_name = os.path.basename(audio_files[index])

            audio = AudioSegment.from_file(f"{input_folder}/{file_name}", format=audio_extension)
            duration = len(audio)

            start_formatted = format_time(*start_time)

            end_time = calculate_next_time(start_time, duration)
            end_time = round_time_to_frame(end_time, frame_duration)

            if (index + 1) % 35 == 0:
                hours, minutes, seconds, milliseconds = end_time
                milliseconds += 40
                if milliseconds >= 1000:
                    milliseconds -= 1000
                    seconds += 1
                    if seconds >= 60:
                        seconds -= 60
                        minutes += 1
                        if minutes >= 60:
                            minutes -= 60
                            hours += 1
                end_time = (hours, minutes, seconds, milliseconds)

            end_formatted = format_time(*end_time)

            sub_file.write(f"{index + 1}\n")
            sub_file.write(f"{start_formatted} --> {end_formatted}\n")
            sub_file.write(f"{phrase[index]}\n\n")

            start_time = end_time
            ends.append(end_formatted)
    if subs:
        with open('sub_2.srt', 'w', encoding='utf-8') as sub_file:
            start_formatted = '00:00:00,000'
            sub_index = 1
            num_end_sentences = 0

            for paragraph_index, paragraph in enumerate(paragraphs_and_sentences):
                count_sentences = len(paragraph)
                num_end_sentences += count_sentences

                end_formatted = ends[num_end_sentences-1]

                sub_file.write(f"{sub_index}\n")
                sub_file.write(f"{start_formatted} --> {end_formatted}\n")
                sub_file.write(f"{' '.join(paragraph)}\n\n")

                sub_index += 1
                start_formatted = end_formatted

    progress_bar.update_progress(count_files)
    if count_files != counf_phrase:
        progress_bar.message_fun(f"Количество аудиофайлов - {count_files}, а количество отрывков в тексте - {counf_phrase}.\nСубтитры были созданы с имеющимися файлами!\nЭто окно можно закрыть!")
    else:
        progress_bar.message_fun(f"Генерация субтитров успешно завершена.\nЭто окно можно закрыть!")