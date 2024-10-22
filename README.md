# Audio/Video Transcription Tool
[中文版本说明](https://github.com/i4leader/audio-video-transcription-tool/blob/main/README_CN.md)

This is a Python-based tool with a graphical user interface (GUI) that allows users to transcribe audio and video files using Azure's Speech-to-Text service. The tool supports various audio and video formats and converts them to WAV format before transcription.

## Features

- **Support for Multiple Formats**: Accepts MP3, WAV, MP4, AVI, MKV, and MOV files.
- **Automatic Conversion**: Converts video files to WAV format using `ffmpeg`.
- **Azure Speech-to-Text Integration**: Utilizes Azure's Speech-to-Text service for accurate transcriptions.
- **User-Friendly GUI**: Easy-to-use interface built with `tkinter`.

## Azure Speech Service Free Tier

Azure Speech Service offers a free tier that includes 5 audio hours free per month for speech-to-text services. This includes:

- **Standard Speech to Text**: 5 audio hours free per month
- **Custom Speech to Text**: 5 audio hours free per month
- **Conversation Transcription Multichannel Audio (Preview)**: 5 audio hours free per month

For more details, please refer to the [Azure Speech Service pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/).


## Requirements

- Python 3.x
- `ffmpeg` (installed and added to system PATH)
- Python packages listed in `requirements.txt`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/audio-video-transcription-tool.git
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
    - Azure Subscription Key(Key for speech service)
    - Region
    - Source File (audio or video)
    - Output File (optional)

3. Click "Start Transcription" to begin the process.

## To Do List

- **Support more speech services**: Integrate with other speech-to-text services like AWS, GCP, or local ones.
- **Support generating subtitles for different languages**: Add functionality to generate subtitles in various languages.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
