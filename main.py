import io
import os
import sys
from uuid import uuid4

import six
import google.cloud.storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

speech_client = speech.SpeechClient()
storage_client = google.cloud.storage.Client()

def gcloud_transcribe_short(config):
    """
    Uses Google Cloud Speech-to-Text to transcribe audio files up 
    to durations of 60 seconds.

    @config: Provided as a dict, requires at minimum:
        - filepath - path to file
        - sample_rate_hertz - gcloud setting, typically 16000
        - language_code - gcloud setting, e.g 'en-AU' or 'ja-JP'
        - encoding - gcloud setting, e.g 
                        enums.RecognitionConfig.AudioEncoding.LINEAR16

        Other examples of config options that might be of use:
        - enable_speaker_diarization=False, diarization_speaker_count=2):
        - enable_word_time_offsets=False

    @return: Response object from Google Cloud Speech
    """
    try:
        file_path = config.pop('filepath')
    except KeyError:
        raise Exception("`filepath` not specified for transcription operation.")

    # Read file into memory before uploading
    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    
    # Detects speech in the audio file
    return speech_client.recognize(config, audio)

def gcloud_transcribe_long(config):
    """
    Uses Google Cloud Speech-to-Text to transcribe audio files beyond
    a duration of 60 seconds. Note that files must be uploaded to Google-
    -Cloud Storage (GCS) before this can be ran. See `gcloud_upload_file`
    for more information.

    @config: Provided as a dict, requires at minimum:
        - remotepath - path to gs://bucket_name/file_path
        - sample_rate_hertz - gcloud setting, typically 16000
        - language_code - gcloud setting, e.g 'en-AU' or 'ja-JP'
        - encoding - gcloud setting, e.g 
                        enums.RecognitionConfig.AudioEncoding.LINEAR16
        - timeout - how long to wait before timing out

        Other examples of config options that might be of use:
        - enable_speaker_diarization=False, diarization_speaker_count=2):
        - enable_word_time_offsets=False

    @return: Response object from Google Cloud Speech
    """
    try:
        remote_path = config.pop('remotepath')
    except KeyError:
        raise Exception("`remotepath` not specified for transcription operation.")

    try:
        timeout = config.pop('timeout')
    except KeyError:
        raise Exception("`timeout` not specified for transcription operation.")

    audio = types.RecognitionAudio(uri=remote_path)
    operation = speech_client.long_running_recognize(config, audio)

    response = operation.result(timeout=timeout)

    return result

def gcloud_upload_file(local_filepath, gcloud_bucket_name):
    """
    Uploads a single file to GCloud Storage in the specified
    bucket.

    @local_filepath: /path/to/file/to/be/uploaded
    @gcloud_bucket_name: remote bucket name set up via GCloud

    @return: remote url of the uploaded file
    """
    bucket = storage_client.get_bucket(gcloud_bucket_name)
    remote_filepath = "%s__%s" % (
                os.path.basename(local_filepath),
                uuid4()
            )

    blob = bucket.blob(remote_filepath)

    # Read the file and upload it
    with io.open(local_filepath, 'rb') as file:
        data = file.read()
        blob.upload_from_string(data)

    url = blob.public_url
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    print("File successfully uploaded to %s" % url)
    return url

params = {
    #'filepath': sys.argv[1],
    'remotepath': 'gs://alveo-transcriber/audio.wav__f3d4e33a-8aac-4562-9247-11495ebcce25',
    'sample_rate_hertz': 16000,
    'language_code': 'en-AU',
    'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16
}
#gcloud_upload_file(sys.argv[1], 'alveo-transcriber')
#print(gcloud_transcribe_short(params))
print(gcloud_transcribe_long(params))
