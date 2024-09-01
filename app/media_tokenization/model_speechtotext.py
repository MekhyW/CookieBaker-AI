import whisper

model = None

def load_model(model_name="base"):
    global model
    model = whisper.load_model(model_name)
    return model

def transcribe(url):
    if model is None:
        raise ValueError("STT model not loaded")
    transcription = model.transcribe(url)['text']
    print(f"Audio transcription: {transcription}")
    return transcription

if __name__ == "__main__":
    load_model()
    model = whisper.load_model("base")
    transcribe("https://www2.cs.uic.edu/~i101/SoundFiles/gettysburg10.wav")