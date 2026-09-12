import yt_dlp
from pydub import AudioSegment
import os 

DOWNLOADS_DIR='downloads'
os.makedirs(DOWNLOADS_DIR , exist_ok=True)

FFMPEG_DIR = r"C:\ffmpeg\bin"

def download_video(url: str):

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "ffmpeg_location": FFMPEG_DIR,
        "overwrites": True, 
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename=ydl.prepare_filename(info)
        wav_path = os.path.splitext(filename)[0] + ".wav"
        print("filename---->",filename)
        return wav_path


def convert_wav(input:str):
    output_path=os.path.splitext(input)
    output_path=output_path[0]+"_converted.wav"
    audio=AudioSegment.from_file(input)
    audio=AudioSegment.set_channels(1).set_frame_rate(16000) # 16khz
    audio.export(output_path,format='wav')
    return output_path

def chunk_audio(wav_path:str,chunk_minute:int=10):
    audio=AudioSegment.from_file(wav_path)
    chunk_ms=chunk_minute*60*1000

    chunks=[]

    for i,chunk in enumerate(range(0,len(audio),chunk_ms)):
        chunk_name=f"{wav_path}_chunk_{i}.wav"
        chunk=audio[chunk:chunk+chunk_ms]
        chunk.export(chunk_name,format='wav')
        chunks.append(chunk_name)

    return chunks


def process_input(source:str):
    if source.startswith("http://") or source.startswith("https://"):
        wav_path=download_video(source)
    else :
        wav_path=convert_wav(source)
    return chunk_audio(wav_path)  

# print(process_input("https://www.youtube.com/shorts/WmeEd3A64AU"))
