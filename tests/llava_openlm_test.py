from openai import OpenAI
import base64
import requests

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
image_url = ""
found_text = ""

def get_base_64_img(image):
    if "http" not in image:
        base64_image = base64.b64encode(open(image, "rb").read()).decode('utf-8')
    else:
        response = requests.get(image)
        base64_image = base64.b64encode(response.content).decode('utf-8')
    return base64_image

completion = client.chat.completions.create(
  model="xtuner/llava-phi-3-mini-gguf",
  messages=[
    {
      "role": "system",
      "content": "You are an assistant that provides very short, concise responses. The assistant ran OCR on the image and found the following text: " + found_text,
    },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": f"Describe the image. Limit your responses to only a few sentences, and avoid any unnecessary elaboration."},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{get_base_64_img(image_url)}",
          },
        },
      ],
    }
  ],
  max_tokens=1000,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content:
    print(chunk.choices[0].delta.content, end="", flush=True)