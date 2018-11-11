import io
import os
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

"""
Uses Google Cloud Speech-to-Text to transcribe audio files up 
to durations of 60 seconds.

@params: Provided as a dict, requires at minimum:
    - filepath - path to file
    - sample_rate_hertz - gcloud setting, typically 16000
    - language_code - gcloud setting, e.g 'en-AU' or 'ja-JP'
    - encoding - gcloud setting, e.g 
                    enums.RecognitionConfig.AudioEncoding.LINEAR16

    Other examples of params that might be of use:
    - enable_speaker_diarization=False, diarization_speaker_count=2):
    - enable_word_time_offsets=False
"""
def auto_transcribe_short(params):
    if params['filepath'] is None:
        raise Exception("`filepath` not specified for segmentation operation.")

    client = speech.SpeechClient()

    # Read file into memory before uploading
    with io.open(params['filepath'], 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    
    # Filter non-Google Cloud parameters
    params.pop('filepath')

    config = types.RecognitionConfig(
        **{k: v for k, v in params.items() if v is not None}
    )

    # Detects speech in the audio file
    return client.recognize(config, audio)

params = {
    'filepath': sys.argv[1],
    'sample_rate_hertz': 16000,
    'language_code': 'en-AU',
    'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16
}
print(auto_transcribe_short(params))
