import os

os.environ["PATH"] = r"C:\ffmpeg\bin;" + os.environ["PATH"]

import whisper
import os 
import requests
from pydub import AudioSegment

whisper_model=os.getenv("WHISPER_MODEL","small")
model=whisper.load_model(whisper_model)

def transcribe_chunk_whisper(chunk_path:str):
    chunk_script=model.transcribe(chunk_path,task='transcribe')
    return chunk_script['text']

def transilble_all_chunk(chunks:list):
    whole_script=''
    for chunk in chunks:
        text=transcribe_chunk_whisper(chunk)
        whole_script+=text + " "
    return whole_script

# from faster_whisper import WhisperModel

# whisper_model_size = os.getenv("WHISPER_MODEL", "small")

# # int8 quantization = much faster on CPU, small accuracy tradeoff (usually negligible)
# model = WhisperModel(
#     whisper_model_size,
#     device="cpu",
#     compute_type="int8",
# )


# def transcribe_chunk_whisper(chunk_path: str) -> str:
#     segments, _ = model.transcribe(
#         chunk_path,
#         task="transcribe",
#         beam_size=1,          
#         vad_filter=True,      # skips silent parts, avoids wasting compute on empty audio
#         vad_parameters=dict(min_silence_duration_ms=500),
#     )
 
#     return "".join(segment.text for segment in segments)


# def transilble_all_chunk(chunks: list):
#     whole_script=""
#     for chunk in chunks:
#         script=transcribe_chunk_whisper(chunk)
#         whole_script+=script + " "
#     return whole_script
