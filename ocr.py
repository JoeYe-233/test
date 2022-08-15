import requests
import time
# STEP 1
import muggle_ocr
import os
# STEP 2
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)

a=requests.get('https://ua.scu.edu.cn/captcha?captchaId=4057950348')
b=a.content
print(b)
st = time.time()
# STEP 3
text = sdk.predict(image_bytes=b)
print(text, time.time() - st)