import tkinter as tk
from tkinter import filedialog, messagebox
import azure.cognitiveservices.speech as speechsdk
import os
from pydub import AudioSegment
from threading import Event
import subprocess

def convert_mp3_to_wav(mp3_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    wav_file_path = os.path.splitext(mp3_file_path)[0] + ".wav"
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def convert_video_to_wav(video_file_path):
    wav_file_path = os.path.splitext(video_file_path)[0] + ".wav"
    command = ["ffmpeg", "-i", video_file_path, "-ar", "16000", "-ac", "1", "-sample_fmt", "s16", wav_file_path]
    subprocess.run(command, check=True)
    return wav_file_path

def transcribe_audio(file_path, subscription_key, region, language="zh-CN", output_file_path=None):
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"File not found: {file_path}")
        return

    try:
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        speech_config.speech_recognition_language = language

        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        transcription_results = []

        def recognized(evt):
            transcription_results.append(evt.result.text)
            print(f"Recognized: {evt.result.text}")

        def session_stopped(evt):
            print("Session stopped")
            done.set()

        def canceled(evt):
            print("Canceled")
            done.set()

        speech_recognizer.recognized.connect(recognized)
        speech_recognizer.session_stopped.connect(session_stopped)
        speech_recognizer.canceled.connect(canceled)

        done = Event()
        speech_recognizer.start_continuous_recognition()
        done.wait()
        speech_recognizer.stop_continuous_recognition()

        if output_file_path is None:
            output_file_path = os.path.splitext(file_path)[0] + ".txt"

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for result in transcription_results:
                output_file.write(result + '\n')

        messagebox.showinfo("Success", f"Transcription saved to {output_file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp3;*.wav;*.mp4;*.avi;*.mkv;*.mov")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def browse_output():
    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if output_path:
        entry_output_path.delete(0, tk.END)
        entry_output_path.insert(0, output_path)

def start_transcription():
    subscription_key = entry_subscription_key.get()
    region = entry_region.get()
    file_path = entry_file_path.get()
    output_path = entry_output_path.get()

    if not subscription_key or not region or not file_path:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    if file_path.endswith(".mp3"):
        file_path = convert_mp3_to_wav(file_path)
    elif file_path.endswith((".mp4", ".avi", ".mkv", ".mov")):
        file_path = convert_video_to_wav(file_path)

    transcribe_audio(file_path, subscription_key, region, "zh-CN", output_path)

# GUI setup
root = tk.Tk()
root.title("Audio/Video Transcription")

tk.Label(root, text="Azure Subscription Key:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_subscription_key = tk.Entry(root, width=50)
entry_subscription_key.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Region:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_region = tk.Entry(root, width=50)
entry_region.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Source File:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_file).grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Output File:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_output_path = tk.Entry(root, width=50)
entry_output_path.grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=3, column=2, padx=10, pady=5)

tk.Button(root, text="Start Transcription", command=start_transcription).grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
