import whisper

model = whisper.load_model("base")
result = model.transcribe("https://www2.cs.uic.edu/~i101/SoundFiles/gettysburg10.wav")
print(result['text'])