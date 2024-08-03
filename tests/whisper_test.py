import whisper

model = whisper.load_model("base")
result = model.transcribe("query.wav")
print(result['text'])