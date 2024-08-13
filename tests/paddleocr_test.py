from paddleocr import PaddleOCR
import requests
from PIL import Image
from io import BytesIO
import numpy as np

def ocr_with_paddle(img):
    finaltext = ''
    ocr = PaddleOCR(lang='en', use_angle_cls=True)
    result = ocr.ocr(img)
    if not result[0]:
        return None
    for i in range(len(result[0])):
        text = result[0][i][1][0]
        finaltext += ' '+ text
    return finaltext

def url_to_ndarray(url):
    response = requests.get(url)
    img = np.array(Image.open(BytesIO(response.content)))
    return img

url = ""
img = url_to_ndarray(url)
print("RESULT: ", ocr_with_paddle(img))