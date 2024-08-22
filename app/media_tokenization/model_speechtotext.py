import whisper

model = None

def load_model(model_name="base"):
    global model
    model = whisper.load_model(model_name)
    return model

def transcribe(url):
    if model is None:
        raise ValueError("STT model not loaded")
    return model.transcribe(url)