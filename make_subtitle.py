import argparse
import json
import math
import os
import re

import openai as openai
import pysrt
import requests
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pydub import AudioSegment


def video_to_audio(video_file, audio_file, work_dir):
    file_to_convert = AudioFileClip(work_dir + "\\" + video_file)
    file_to_convert.write_audiofile(work_dir + "\\" + audio_file)
    file_to_convert.close()


# 将音频文件切割成固定大小的小文件
def split_audio_file(input_file, output_directory, chunk_size):
    # 加载音频文件
    audio = AudioSegment.from_file(output_directory + "\\" + input_file)

    # 获取音频文件时长
    duration_in_sec = math.ceil(audio.duration_seconds)

    # 计算需要切割成的小文件数量
    num_chunks = math.ceil((os.path.getsize(output_directory + "\\" + input_file) / 1024 / 1024) / chunk_size)

    # 计算每个小文件的长度
    chunk_length = duration_in_sec / num_chunks

    # 切割音频文件
    for i in range(num_chunks):
        start_time = i * chunk_length * 1000  # 转换为毫秒
        end_time = start_time + chunk_length * 1000
        chunk = audio[start_time:end_time]

        # 保存切割后的小文件
        output_file = os.path.join(output_directory, f"chunk_{i + 1}.mp3")
        chunk.export(output_file, format="mp3")

    return num_chunks


def transcribe_single_audio(api_key, audio_file, new_file_path, src_language):
    audio_file = open(audio_file, "rb")
    openai.api_key = api_key
    transcript = openai.Audio.translate("whisper-1", audio_file, response_format="srt", language=src_language)
    f = open(new_file_path, "a+", encoding="utf-8")
    f.write(transcript)
    f.close()
    print(new_file_path + " " + "complete")


def get_all_srt(api_key, basic_file_path, src_language, size):
    for i in range(1, size + 1):
        transcribe_single_audio(api_key, basic_file_path + "\\chunk_%s.mp3" % str(i),
                                basic_file_path + "\\chunk_%s.srt" % str(i), src_language)


def translate_all_subtitle(api_key, basic_file_path, language, size):
    for i in range(1, size + 1):
        translate_subtitle(api_key, basic_file_path, basic_file_path + "\\chunk_%s.srt" % str(i), language, i)


def translate_subtitle(api_key, basic_file_path, file_path, language, size):
    srt = pysrt.open(file_path)
    for i in srt:
        try:
            tran_text = translate_turbo(api_key, i.text, language)
            i.text = tran_text
            srt.save(basic_file_path + "\\chunk_new_%s.srt" % str(size), encoding="utf-8")
        except Exception as e:
            print(e)
            continue


def translate_turbo(api_key, text, language):
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Please help me translate: `{text}` to {language},no other words",
            }
        ],
    )
    t_text = (
        completion["choices"][0]
        .get("message")
        .get("content")
        .encode("utf8")
        .decode()
    )
    print(t_text)
    return t_text


def translate_davinci(api_key, text, language):
    api_url = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "prompt": f"Please help me translate: `{text}` to {language},no other words",
        "model": "text-davinci-003",
        "max_tokens": 2048,
        "temperature": 1,
        "top_p": 1,
    }
    r = requests.post(api_url, headers=headers, json=data)
    print(r.text)
    r = r.json()
    t_text = (
        r["choices"][0]
        .get("text")
        .encode("utf8")
        .decode()
    )

    return t_text


def joint_srt(work_dir, size):
    f = open(work_dir + "\\result.srt", "a+")
    result_srt = pysrt.open(work_dir + "\\result.srt")
    index = 1
    for i in range(1, size + 1):
        chunk_srt = pysrt.open(work_dir + "\\chunk_new_%s.srt" % i)
        chunk_srt.shift(seconds=(i - 1) * 60 * 10)
        for j in chunk_srt:
            j.index = index
            result_srt.append(j)
            index = index + 1
        result_srt.save()


def main(api_key, work_dir, video_file, audio_file, src_language, language):
    minute = 10
    # num_chunks = 2
    video_to_audio(video_file, audio_file, work_dir)
    num_chunks = split_audio_file(audio_file, work_dir, minute)
    get_all_srt(api_key, work_dir, src_language, num_chunks)
    translate_all_subtitle(api_key, work_dir, language, num_chunks)
    joint_srt(work_dir, num_chunks)


def check_api_key(api_key):
    openai.api_key = api_key
    completion = openai.Completion.create(
        engine="davinci",
        prompt="Hello",
        temperature=0,
        max_tokens=1,
    )
    print(completion)

    print("API key is valid.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    audio_file_path = "mp3file.mp3"

    parser.add_argument(
        "--api_key",
        dest="api_key",
        type=str,
        help="OpenAI API Key",
    )

    parser.add_argument(
        "--work_dir",
        dest="work_dir",
        type=str,
        help="work directory，all the file will be saved here",
    )

    parser.add_argument(
        "--video_file",
        dest="video_file",
        type=str,
        help="video_file_path",
    )

    parser.add_argument(
        "--src_language",
        dest="src_language",
        type=str,
        help="src_language",
    )

    parser.add_argument(
        "--dest_language",
        dest="dest_language",
        type=str,
        help="dest_language",
    )

    parser.add_argument(
        "--proxy",
        dest="proxy",
        type=str,
        help="proxy,like http://127.0.0.1:7890",
    )


    options = parser.parse_args()
    api_key = options.api_key
    work_dir = options.work_dir
    video_file = options.video_file
    src_language = options.src_language
    dest_language = options.dest_language
    proxy = options.proxy
    if proxy:
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy

    main(api_key, work_dir, video_file, audio_file_path, src_language, dest_language)
