# 音频/视频转录工具

[English Version](https://github.com/i4leader/audio-video-transcription-tool/blob/main/README.md)

这是一个基于Python的工具，具有图形用户界面（GUI），允许用户使用Azure的语音转文字服务转录音频和视频文件。该工具支持多种音频和视频格式，并在转录前将其转换为WAV格式。

## 功能

- **支持多种格式**：接受MP3、WAV、MP4、AVI、MKV和MOV文件。
- **自动转换**：使用`ffmpeg`将视频文件转换为WAV格式。
- **Azure语音转文字集成**：利用Azure的语音转文字服务进行准确的转录。
- **用户友好的GUI**：使用`tkinter`构建的易用界面。

## Azure语音服务免费层

Azure语音服务提供每月5小时的免费语音转文字服务。具体包括：

- **标准语音转文字**：每月5小时免费
- **自定义语音转文字**：每月5小时免费
- **对话转录多通道音频（预览版）**：每月5小时免费

有关详细信息，请参阅[Azure语音服务定价](https://azure.microsoft.com/zh-cn/pricing/details/cognitive-services/speech-services/)。

## 要求

- Python 3.x
- `ffmpeg`（已安装并添加到系统PATH中）
- `requirements.txt`中列出的Python包

## 安装

1. 克隆仓库：
    ```bash
    git clone https://github.com/i4leader/audio-video-transcription-tool.git
    cd audio-video-transcription-tool
    ```

2. 安装所需的Python包：
    ```bash
    pip install -r requirements.txt
    ```

3. 确保`ffmpeg`已安装并可从命令行访问。你可以从[FFmpeg的官方网站](https://ffmpeg.org/download.html)下载。

## 使用

1. 运行脚本：
    ```bash
    python transcription_tool.py
    ```

2. 在GUI中填写所需字段：
    - Azure订阅密钥（即Azure Speech 服务的密钥）
    - 区域
    - 源文件（音频或视频）
    - 输出文件（可选）

3. 点击“开始转录”开始处理。

## 待办事项

- **支持更多语音服务**：集成其他语音转文字服务，如AWS、GCP或本地服务。
- **支持生成不同语言的字幕**：增加生成各种语言字幕的功能。

## 许可证

此项目根据Apache License 2.0许可。详情请参阅[LICENSE](LICENSE)文件。
