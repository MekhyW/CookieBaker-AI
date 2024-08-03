from paddleocr import PaddleOCR

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

img = 'Captura de tela 2024-07-15 215658.png'
print("RESULT: ", ocr_with_paddle(img))