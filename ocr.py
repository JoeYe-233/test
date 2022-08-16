# import requests
# import time
# # STEP 1
# import muggle_ocr
# import os
# # STEP 2
# sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
# print('data={')
# for i in range(1,10):
#     a=requests.get('https://ua.scu.edu.cn/captcha?captchaId=4057950348')
#     b=a.content
#     st = time.time()
#     # STEP 3
#     text = sdk.predict(image_bytes=b)
#     print("\'"+text+"\':bytearray("+str(b)+"),")
# print('}')

import base64
import json
import logging
import re
import time
import os
import bs4
import requests
import hashlib


UA_captcha_url = r'https://ua.scu.edu.cn/captcha?captchaId=4057950348'
captcha_break_url = r'http://localhost:19952/captcha/v1'


img_response = requests.get(UA_captcha_url)
if img_response.status_code == requests.codes['ok']:
        print(f"成功获取验证码图片\t\t\t\t<httpRespond>[{img_response.status_code}]")
        # print("成功获取验证码图片\t\t\t", end='')
else:
        print(f"获取图片失败\t\t\t<httpRespond>[{img_response.status_code}]")


print(f"将图片转发至本地验证码服务器...\t\t{captcha_break_url}")
# print("将图片转发至本地验证码服务器...\t\t%s" % captcha_break_url)
break_time = time.time()
base64EncodedStr = base64.b64encode(img_response.content)
captcha_to_break = {
    'image': base64EncodedStr.decode('utf-8')
}
captcha_break_response = requests.post(captcha_break_url, json=captcha_to_break)
captcha_break = json.loads(captcha_break_response.text)
break_time = time.time() - break_time
if captcha_break_response.status_code == requests.codes['ok']:
    print(f"获取预测验证码成功\t预测结果为: {captcha_break['message']} \t[{break_time:.3f}s]")
    # print("获取预测验证码成功\t", end='')
else:
    print(f"获取预测失败")
    # print("获取预测失败\t", end='')