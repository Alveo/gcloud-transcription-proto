# Google Speech-to-Text API prototype
Important: Only support audio up to one minunte in duration.

## Setup
```bash
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```
## Configuration
Retrieve your Google Cloud credentials in json form and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to it, alternatively dump it as `cred.json` in the working directory and `source environment`.

## Execution
`python main.py /path/to/audio/file`
