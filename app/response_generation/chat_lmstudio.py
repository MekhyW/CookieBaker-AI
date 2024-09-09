# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="bartowski/gemma-2-2b-it-abliterated-GGUF",
  messages=[
    {"role": "system", "content": "Sempre responda em rimas."},
    {"role": "user", "content": "Apresente-se."}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)