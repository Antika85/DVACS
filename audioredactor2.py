import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tkinter import messagebox
from pydub import AudioSegment
import numpy as np
from scipy.ndimage import label

from progress_bar_script import ProgressBar

output_folder = "result"

def clean_result_folder():
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, file))
    else:
        os.makedirs(output_folder)


def remove_extra_silence(audio, silence_threshold, sample_duration_ms, buffer_ms):
    samples = np.array(audio.get_array_of_samples())

    # Удаляем пустоту в начале
    first_sample_index = next((i for i, sample in enumerate(samples) if abs(sample) >= silence_threshold), 0)
    start_time = max(0, first_sample_index * sample_duration_ms - buffer_ms)

    # Удаляем пустоту в конце
    last_sample_index = next((i for i, sample in enumerate(reversed(samples)) if abs(sample) >= silence_threshold), 0)
    end_time = min(len(audio), len(audio) - last_sample_index * sample_duration_ms + buffer_ms)

    # Возвращаем аудио без лишней тишины
    return audio[start_time:end_time]


def process_file_chunked(file_name, silence_threshold, audio_extension, input_folder, min_silence_duration_ms=100, padding_ms=40, chunk_size=1000):
    input_path = f"{input_folder}/{file_name}"
    audio = AudioSegment.from_file(input_path, format=audio_extension)

    total_duration = len(audio)
    non_silence_audio = AudioSegment.silent(duration=0)

    for start in range(0, total_duration, chunk_size):
        end = min(start + chunk_size, total_duration)
        chunk = audio[start:end]

        samples = np.abs(np.array(chunk.get_array_of_samples()))
        silence_mask = samples < silence_threshold

        labeled_silence, num_features = label(silence_mask)
        silence_intervals = []

        sample_duration_ms = 1000.0 / chunk.frame_rate
        min_silence_samples = int(min_silence_duration_ms / sample_duration_ms)

        for i in range(1, num_features + 1):
            region = np.where(labeled_silence == i)[0]
            if len(region) >= min_silence_samples:
                start_time = region[0] * sample_duration_ms
                end_time = region[-1] * sample_duration_ms
                silence_intervals.append((start_time + padding_ms, end_time - padding_ms))

        last_end = 0
        for start_time, end_time in silence_intervals:
            non_silence_audio += chunk[last_end:start_time]
            last_end = end_time
        non_silence_audio += chunk[last_end:]

    buffer_ms = 50  # Буфер в миллисекундах, оставляем 100 мс в начале и конце
    non_silence_audio = remove_extra_silence(non_silence_audio, silence_threshold, 1000.0 / audio.frame_rate, buffer_ms=buffer_ms)

    # Сохранение результата
    output_path = f"{output_folder}/new_{file_name}"
    non_silence_audio.export(output_path, format=audio_extension)

def process_files_in_parallel(silence_threshold, audio_extension, input_folder):
    try:
        start_time = time.time()
        audio_files = [f for f in os.listdir(input_folder) if f.endswith(f'.{audio_extension}')]
        count_audiofiles = len(audio_files)
        clean_result_folder()

        progress_bar = ProgressBar(max_value=count_audiofiles, name_process='Удаление пауз')
        current_num_audiofile = 0
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(process_file_chunked, file_name, silence_threshold, audio_extension, input_folder) for file_name in audio_files]
            for future in as_completed(futures):
                future.result()
                current_num_audiofile += 1
                progress_bar.update_progress(current_num_audiofile)

        end_time = time.time()
        execution_time = int(end_time - start_time)
        progress_bar.message_fun(f"Программа была выполнена за {execution_time} секунд.\nАудиофайлы сохранены в папку {output_folder}.\nЭто окно можно закрыть!")
    except Exception as ex:
        messagebox.showerror("Ошибка", f"Произошла неизвестная ошибка, покажите её автору: {ex}")
