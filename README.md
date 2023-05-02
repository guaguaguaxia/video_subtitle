**[中文](./README-CN.md) | English**

# OpenAI Whisper Video Subtitle Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/guaguaguaxia/video_subtitle.svg)](https://github.com/guaguaguaxia/video_subtitle/issues)
[![Forks](https://img.shields.io/github/forks/guaguaguaxia/video_subtitle.svg)](https://github.com/guaguaguaxia/video_subtitle/network)
[![Stars](https://img.shields.io/github/stars/guaguaguaxia/video_subtitle.svg)](https://github.com/guaguaguaxia/video_subtitle/stargazers)

The OpenAI Whisper Video Subtitle Generator is a project that utilizes the OpenAI Whisper API to generate subtitles in any language for any video. The goal of this project is to help users easily create multilingual subtitles for video content, increasing the accessibility and reach of the videos.


### how to use
1. Clone the repository and ensure you have python enviroment and OpenAI api key
2. make sure you have installed ffmpeg and configured the environment variables
3. Run the following command
```
python make_subtitle.py --api_key xxx --work_dir xxx --video_file xxx --src_language en --dest_language chinese --proxy xx
```

### parameter explain
- api_key: OpenAI api key,like `sk-xxx,sk-xxx,sk-xxx`
- work_dir: the directory to save the all the files 
- video_file: the video file name,like xxx.mp4
- src_language: the source language of the video,like `en`
- dest_language: the language you want to generate,like chinese,english
- proxy: the proxy to use,like `http://127.0.0.1:7890`