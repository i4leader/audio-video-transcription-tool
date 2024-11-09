import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import azure.cognitiveservices.speech as speechsdk
import os
from pydub import AudioSegment
from threading import Event
import subprocess
import json

# 加载之前的设置
def load_settings():
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# 保存当前设置
def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file)

# 将MP3转换为WAV格式
def convert_mp3_to_wav(mp3_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    wav_file_path = os.path.splitext(mp3_file_path)[0] + ".wav"
    audio.export(wav_file_path, format="wav")
    return wav_file_path

# 将视频转换为WAV格式
def convert_video_to_wav(video_file_path):
    wav_file_path = os.path.splitext(video_file_path)[0] + ".wav"
    command = ["ffmpeg", "-i", video_file_path, "-ar", "16000", "-ac", "1", "-sample_fmt", "s16", wav_file_path]
    subprocess.run(command, check=True)
    return wav_file_path

# 使用Azure认知服务转录音频
def transcribe_audio(file_path, subscription_key, region, language="zh-CN", output_file_path=None):
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"File not found: {file_path}")
        return

    try:
        # 配置Azure语音服务
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        speech_config.speech_recognition_language = language
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        transcription_results = []

        # 语音识别事件处理程序
        def recognized(evt):
            result = evt.result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                transcription_results.append({
                    "text": result.text,
                    "start_time": result.offset / 10_000_000,  # 转换为秒
                    "duration": result.duration / 10_000_000  # 转换为秒
                })
                print(f"Recognized: {result.text}")

        def session_stopped(evt):
            print("Session stopped")
            done.set()

        def canceled(evt):
            print("Canceled")
            done.set()

        # 连接事件处理程序
        speech_recognizer.recognized.connect(recognized)
        speech_recognizer.session_stopped.connect(session_stopped)
        speech_recognizer.canceled.connect(canceled)

        done = Event()
        speech_recognizer.start_continuous_recognition()
        done.wait()
        speech_recognizer.stop_continuous_recognition()

        # 保存转录结果到SRT文件
        if output_file_path is None:
            output_file_path = os.path.splitext(file_path)[0] + ".srt"

        save_transcription_results(output_file_path, transcription_results)

        messagebox.showinfo("Success", f"Transcription saved to {output_file_path}")

    except FileNotFoundError as e:
        messagebox.showerror("Error", f"File not found: {e}")
    except speechsdk.SpeechSDKException as e:
        messagebox.showerror("Error", f"Speech SDK error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# 保存转录结果到SRT文件
def save_transcription_results(output_file_path, transcription_results):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        subtitle_index = 1
        for result in transcription_results:
            start_time = result["start_time"]
            end_time = start_time + result["duration"]
            text = result["text"]

            # 如果文本超过30个单词或10秒，则将其拆分为较小的块
            words = text.split()
            max_words_per_subtitle = 30
            max_duration_per_subtitle = 10

            for i in range(0, len(words), max_words_per_subtitle):
                chunk = words[i:i + max_words_per_subtitle]
                chunk_text = ' '.join(chunk)
                chunk_start_time = start_time + (i / max_words_per_subtitle) * max_duration_per_subtitle
                chunk_end_time = min(chunk_start_time + max_duration_per_subtitle, end_time)

                output_file.write(f"{subtitle_index}\n")
                output_file.write(f"{format_time(chunk_start_time)} --> {format_time(chunk_end_time)}\n")
                output_file.write(f"{chunk_text}\n\n")
                subtitle_index += 1

# 格式化时间
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# 浏览输入文件
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp3;*.wav;*.mp4;*.avi;*.mkv;*.mov")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# 浏览输出文件
def browse_output():
    output_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("Subtitle Files", "*.srt")])
    if output_path:
        entry_output_path.delete(0, tk.END)
        entry_output_path.insert(0, output_path)

# 开始转录过程
def start_transcription():
    subscription_key = entry_subscription_key.get()
    region = region_var.get()
    language = language_var.get()
    file_path = entry_file_path.get()
    output_path = entry_output_path.get()

    if not subscription_key or not region or not file_path:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # 如果需要，将文件转换为WAV
    if file_path.endswith(".mp3"):
        file_path = convert_mp3_to_wav(file_path)
    elif file_path.endswith((".mp4", ".avi", ".mkv", ".mov")):
        file_path = convert_video_to_wav(file_path)

    transcribe_audio(file_path, subscription_key, region, language, output_path)

    # 保存设置
    settings = {
        "subscription_key": subscription_key,
        "region": region,
        "language": language,
        "file_path": file_path,
        "output_path": output_path
    }
    save_settings(settings)

# GUI设置
root = tk.Tk()
root.title("Audio/Video Transcription")

settings = load_settings()

# Azure订阅密钥输入
tk.Label(root, text="Azure Subscription Key:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_subscription_key = tk.Entry(root, width=50, show="*")
entry_subscription_key.grid(row=0, column=1, padx=10, pady=5)
entry_subscription_key.insert(0, settings.get("subscription_key", ""))

def toggle_key_visibility():
    if entry_subscription_key.cget('show') == '*':
        entry_subscription_key.config(show='')
        btn_toggle_key.config(text="Hide Key")
    else:
        entry_subscription_key.config(show='*')
        btn_toggle_key.config(text="Show Key")

btn_toggle_key = tk.Button(root, text="Show Key", command=toggle_key_visibility)
btn_toggle_key.grid(row=0, column=2, padx=10, pady=5)

# 区域输入
tk.Label(root, text="Region:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
region_var = tk.StringVar(value=settings.get("region", ""))
region_menu = ttk.Combobox(root, textvariable=region_var, values=["eastus", "westus", "centralus", "eastasia", "southeastasia"])
region_menu.grid(row=1, column=1, padx=10, pady=5)

# 语言输入
tk.Label(root, text="Language:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
language_var = tk.StringVar(value=settings.get("language", "zh-CN"))
language_menu = ttk.Combobox(root, textvariable=language_var, values=["zh-CN", "en-US", "fr-FR", "de-DE", "es-ES"])
language_menu.grid(row=2, column=1, padx=10, pady=5)

# 源文件输入
tk.Label(root, text="Source File:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=3, column=1, padx=10, pady=5)
entry_file_path.insert(0, settings.get("file_path", ""))
tk.Button(root, text="Browse", command=browse_file).grid(row=3, column=2, padx=10, pady=5)

# 输出文件输入
tk.Label(root, text="Output File:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_output_path = tk.Entry(root, width=50)
entry_output_path.grid(row=4, column=1, padx=10, pady=5)
entry_output_path.insert(0, settings.get("output_path", ""))
tk.Button(root, text="Browse", command=browse_output).grid(row=4, column=2, padx=10, pady=5)

# 开始转录按钮
tk.Button(root, text="Start Transcription", command=start_transcription).grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()