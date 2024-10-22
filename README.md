# Audio/Video Transcription Tool

This is a Python-based tool with a graphical user interface (GUI) that allows users to transcribe audio and video files using Azure's Speech-to-Text service. The tool supports various audio and video formats and converts them to WAV format before transcription.

## Features

- **Support for Multiple Formats**: Accepts MP3, WAV, MP4, AVI, MKV, and MOV files.
- **Automatic Conversion**: Converts video files to WAV format using `ffmpeg`.
- **Azure Speech-to-Text Integration**: Utilizes Azure's Speech-to-Text service for accurate transcriptions.
- **User-Friendly GUI**: Easy-to-use interface built with `tkinter`.

## Requirements

- Python 3.x
- `ffmpeg` (installed and added to system PATH)
- Python packages listed in `requirements.txt`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/i4leader/audio-video-transcription-tool.git
    cd audio-video-transcription-tool
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `ffmpeg` is installed and accessible from the command line. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Usage

1. Run the script:
    ```bash
    python transcription_tool.py
    ```

2. Fill in the required fields in the GUI:
    - Azure Subscription Key
    - Region
    - Source File (audio or video)
    - Output File (optional)

3. Click "Start Transcription" to begin the process.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
