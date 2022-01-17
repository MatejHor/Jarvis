#!/usr/bin/python
from pytube import YouTube
import argparse
import re

parser = argparse.ArgumentParser(description='Youtube downloader')
parser.add_argument('-u', '--url', default="https://www.youtube.com/watch?v=oXgtGQq-3V0",
                    help='Url for video to download', type=str)
parser.add_argument('-d', '--destination_path', default='', help='Path to destination file')
parser.add_argument('-f', '--format', default='video/mp4', help='Format to download')
parser.add_argument('-l', '--list_format', action='store_true', help='List of available format')
parser.add_argument('-t', '--tag', default='', help='Tag for download')

args = parser.parse_args()
url = args.url
destination_path = args.destination_path
format = args.format
list_format = args.list_format
tag = args.tag



video = YouTube(url)
if list_format:
    print(f'[+] List of available format for {url}')
    print('[+] Video')
    for stream in video.streams.filter(only_video=True):
        print(f'[+] {stream}')
    print('[+] Audio')
    for stream in video.streams.filter(only_audio=True):
        print(f'[+] {stream}')
    exit()

if tag != '':
    ys = video.streams.get_by_itag(int(tag))
else:
    for video_stream in video.streams:
        if video_stream.mime_type == format:   
            print(f"[+] Downloading video with tag {tag} into {destination_path}")
            ys = video.streams.get_by_itag(int(video_stream.itag))
            break

ys.download(destination_path)
