import ollama
from paddleocr import PaddleOCR
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import base64

image_describer_model = "0ssamaak0/xtuner-llava:phi3-mini-int4"

def check_pull_model(model_name=image_describer_model):
    try:
        models = ollama.list()['models']
        for model in models:
            if model_name == model['name']:
                return model_name
        ollama.pull(model_name)
    except Exception as e:
        print(f"Error in checking/pulling model: {e}")
        raise
    return model_name

def ocr_with_paddle(img):
    finaltext = ''
    ocr = PaddleOCR(lang='en', use_angle_cls=True)
    result = ocr.ocr(img)
    if not result or not result[0]:
        return None
    for line in result[0]:
        text = line[1][0]
        finaltext += ' ' + text
    return finaltext.strip()

def url_to_ndarray(url):
    response = requests.get(url)
    img_bytes = BytesIO(response.content)
    img = np.array(Image.open(img_bytes))
    return img

def get_base_64_img(image):
    if "http" not in image:
        base64_image = base64.b64encode(open(image, "rb").read()).decode('utf-8')
    else:
        response = requests.get(image)
        base64_image = base64.b64encode(response.content).decode('utf-8')
    return base64_image

def describe(url):
    image = url_to_ndarray(url)
    image_base64 = get_base_64_img(url)
    text_in_image = ocr_with_paddle(image)
    print(f"Text in image: {text_in_image}")
    system_prompt = "You are an assistant that provides very short, concise responses."
    if text_in_image:
        system_prompt += f" The assistant ran OCR on the image and found the following text: {text_in_image}"
    user_prompt = "Describe the image. Limit your responses to only a few sentences, and avoid any unnecessary elaboration."
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
            "images": [image_base64]
        }
    ]
    response = ollama.chat(
        model=image_describer_model,
        messages=messages,
        stream=False,
        options={"num_predict": 1000}
    )
    answer = response['message']['content']
    print(f"Response: {answer}")
    return answer

if __name__ == "__main__":
    url = "https://i.ytimg.com/vi/TIxt9guMbXo/maxresdefault.jpg"
    check_pull_model()
    describe(url)
