from pytube import YouTube

import pprint

link = input('Insert link: ')
video = YouTube(link or 'https://www.youtube.com/watch?v=9ao4FEaDGhQ&list=RD9ao4FEaDGhQ&start_radio=1')

for stream in video.streams:
    print(stream)

print('Only audio')
for stream in video.streams.filter(only_audio=True):
    print(stream)

tag = input('Write tag to download ')

ys = video.streams.get_by_itag(int(tag))

ys.download()
