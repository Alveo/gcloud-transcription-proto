import io
import os
import sys
from uuid import uuid4

import six
import google.cloud.storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def gcloud_transcribe_short(params):
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

    @return: Response object from Google Cloud Speech
    """
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

def gcloud_upload_file(local_filepath, gcloud_bucket_name):
    """
    Uploads a single file to GCloud Storage in the specified
    bucket.

    @local_filepath: /path/to/file/to/be/uploaded
    @gcloud_bucket_name: remote bucket name set up via GCloud

    @return: remote url of the uploaded file
    """
    storage_client = google.cloud.storage.Client()
    bucket = storage_client.get_bucket(gcloud_bucket_name)
    remote_filepath = "%s__%s" % (
                os.path.basename(local_filepath),
                uuid4()
            )

    blob = bucket.blob(remote_filepath)
    print("Uploading `%s` as `%s`..." % 
            (local_filepath, remote_filepath))

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
    'filepath': sys.argv[1],
    'sample_rate_hertz': 16000,
    'language_code': 'en-AU',
    'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16
}
#gcloud_upload_file(sys.argv[1], 'alveo-transcriber')
print(auto_transcribe_short(params))
