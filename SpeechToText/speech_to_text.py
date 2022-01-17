#!/usr/bin/python
import argparse
import speech_recognition as sr 
from pydub import AudioSegment
import os
from pydub.silence import split_on_silence

r = sr.Recognizer()

def get_audio_transcription(path):
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )

    folder_name = "audio-chunks-tmp"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
        
        os.remove(os.path.join(folder_name, f"chunk{i}.wav"))
    os.rmdir(folder_name)
    return whole_text

def parse_audio(source):
    wav = "".join(source.split('.')[0:-1]) + '.wav'                               

    if source.endswith('.mp3') or source.endswith('.MP3'):
        audSeg = AudioSegment.from_mp3(source)
    elif source.endswith('.wav') or source.endswith('.WAV'):
        audSeg = AudioSegment.from_wav(source)
    elif source.endswith('.ogg'):
        audSeg = AudioSegment.from_ogg(source)
    elif source.endswith('.flac'):
        audSeg = AudioSegment.from_file(source, "flac")
    elif source.endswith('.3gp'):
        audSeg = AudioSegment.from_file(source, "3gp")
    elif source.endswith('.3g'):
        audSeg = AudioSegment.from_file(source, "3gp")

    audSeg.export(wav, format="wav")
    return wav


parser = argparse.ArgumentParser(description='SpeechToText parser')
parser.add_argument('-p', '--path', default="D:/MyData/Jarvis/SpeechToText/nahravka.mp3",
                    help='Path to file to translate into script', type=str)
parser.add_argument('-d', '--destination_path', default='./speech_to_text.txt', help='Path to destination file')

args = parser.parse_args()
source = args.path
destination = args.destination_path
print(f'[+] Source {source} Destination {destination}')

try: 
    print('[+] Parse source into WAV fromat')
    wav_source = parse_audio(source)

    print('[+] Start processing transcription')
    result = get_audio_transcription(wav_source)

    with open(destination, 'w') as f:
        f.write(result)
finally:
    os.remove(wav_source) if os.path.exists(wav_source) else None
