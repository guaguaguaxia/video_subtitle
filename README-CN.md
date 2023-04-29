# OpenAI Whisper Video Subtitle Generator



[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/guaguaguaxia/video_subtitle.svg)](https://github.com/guaguaguaxia/video_subtitle/issues)
[![Forks](https://img.shields.io/github/forks/guaguaguaxia/video_subtitle.svg)](https://github.com/guaguaguaxia/video_subtitle/network)
[![Stars](https://img.shields.io/github/stars/guaguaguaxia/video_subtitle.svg)](https://github.com/guaguaguaxia/video_subtitle/stargazers)

OpenAI Whisper 视频字幕生成器是一个利用 OpenAI Whisper API 为任何视频生成任何语言的字幕的项目。

### 使用方法
1. 隆代码库并确保您有 python 环境和 OpenAI api key。
2. 运行以下命令：
```
python make_subtitle.py --api_key xxx --work_dir xxx --video_file xxx --src_language en --dest_language chinese --proxy xx
```

### 参数说明
- api_key: OpenAI api key ，例如 `sk-xxx,sk-xxx,sk-xxx`
- work_dir: 保存所有临时文件的目录
- video_file: 视频文件名，例如 xxx.mp4
- src_language: 视频的源语言,比如 `english`、`japanese` 等
- dest_language: 您想要生成的语言，如 `chinese`、`english` 等
- proxy: 要使用的代理，比如 `http://127.0.0.1:7890`