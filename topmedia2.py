import librosa
import soundfile as sf
import os
from tkinter import messagebox

from progress_bar_script import ProgressBar

output_folder = "audiofiles_from_topmedia"

def clean_output_folder():
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, file))
    else:
        os.makedirs(output_folder)

def detect_silence(audio_path, index_file, silence_threshold=-40, min_silence_duration_ms=2800, sample_rate=22050):
    audio, sr = librosa.load(audio_path, sr=sample_rate)

    min_silence_samples = int(min_silence_duration_ms * sr / 1000)
    silence_thresh_amplitude = 10 ** (silence_threshold / 20)

    silent_ranges = []
    silence_start = None

    for i in range(len(audio)):
        if abs(audio[i]) < silence_thresh_amplitude:
            if silence_start is None:
                silence_start = i
        else:
            if silence_start is not None and (i - silence_start) >= min_silence_samples:
                silent_ranges.append((silence_start, i))
            silence_start = None

    start_fragment = 0

    for start_pause, end_pause in silent_ranges:
        start_ms = start_pause * 1000 // sr
        end_ms = end_pause * 1000 // sr

        end_fragment = start_ms + 2000
        fragment = audio[start_fragment * sr // 1000: end_fragment * sr // 1000]
        audio_file = os.path.join(output_folder, f"audio({index_file}).wav")
        sf.write(audio_file, fragment, sr)

        start_fragment = end_ms - 2000
        index_file += 1

    end_fragment = len(audio)
    fragment = audio[start_fragment * sr // 1000: end_fragment * sr // 1000]
    audio_file = os.path.join(output_folder, f"audio({index_file}).wav")
    sf.write(audio_file, fragment, sr)
    index_file += 1
    return index_file

def topmedia2_fun(files):
    try:
        clean_output_folder()
        index_file = 1
        audio_files = sorted(files, key=lambda x: int(x.split('/')[-1].split('.')[0]))
        count_audiofiles = len(audio_files)
        progress_bar = ProgressBar(max_value=count_audiofiles, name_process='Разделение аудио')
        current_num_audiofile = 0
        for audio_file in audio_files:
            index_file = detect_silence(audio_file, index_file)
            current_num_audiofile += 1
            progress_bar.update_progress(current_num_audiofile)

        progress_bar.message_fun(f"Аудиофайлы сохранены в папку {output_folder}.\nЭто окно можно закрыть!")
    except Exception as ex:
        messagebox.showerror("Ошибка", f"Произошла неизвестная ошибка, покажите её автору: {ex}")
