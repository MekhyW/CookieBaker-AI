import model_imagedescriber
import model_speechtotext
import ffmpeg
import tempfile
import os
import mimetypes
import requests

def get_mime_type(url):
    if url.startswith(('http://', 'https://')):
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                mime_type = response.headers.get('Content-Type')
                return mime_type
            else:
                print(f"Failed to retrieve URL: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
    else:
        mime_type, _ = mimetypes.guess_type(url)
        return mime_type

def determine_file_type(url):
    mime_type = get_mime_type(url)
    if mime_type:
        if mime_type.startswith('image/'):
            return "Image"
        elif mime_type.startswith('video/'):
            return "Video"
        elif mime_type.startswith('audio/'):
            return "Audio"
        else:
            return "Other"
    else:
        return "Unknown"
    
def process_audio(url):
    if model_speechtotext.model is None:
        model_speechtotext.load_model()
    result = model_speechtotext.transcribe(url)
    return {"transcribed_audio": result}

def process_image(url):
    if model_imagedescriber.model is None:
        model_imagedescriber.load_model()
    result = model_imagedescriber.describe(url)
    return {"image_description": result}

def process_video(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, "extracted_audio.wav")
        image_path = os.path.join(temp_dir, "first_frame.png")
        ffmpeg.input(url, ss=0).output(image_path, vframes=1).run(quiet=True)
        ffmpeg.input(url).output(audio_path).run(quiet=True)
        image_result = process_image(image_path)
        audio_result = process_audio(audio_path)
    return {"image_description": image_result, "transcribed_audio": audio_result}

def process(url):
    file_type = determine_file_type(url)
    if file_type == "Image":
        return process_image(url)
    elif file_type == "Video":
        return process_video(url)
    elif file_type == "Audio":
        return process_audio(url)
    return None