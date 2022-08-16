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
import time
import requests


UA_captcha_url = r'https://ua.scu.edu.cn/captcha?captchaId=4057950348'
captcha_break_url = r'http://localhost:19952/captcha/v1'



import time
import json
import tornado.log
from tornado.escape import json_encode
from interface import InterfaceManager
from utils import ImageUtils



interface_manager = InterfaceManager()


def run(input):
    bytes_batch, response = ImageUtils.get_bytes_batch(input)
    image_sample = bytes_batch[0]
    image_size = ImageUtils.size_of_image(image_sample)
    size_string = "{}x{}".format(image_size[0], image_size[1])
    interface = interface_manager.get_by_size(size_string)

    split_char = interface.model_conf.split_char



    image_batch, response = ImageUtils.get_image_batch(interface.model_conf, bytes_batch)


    result = interface.predict_batch(image_batch, split_char)
    response['message'] = result
    print(json_encode(response))
    return result



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
Result=run(base64EncodedStr.decode('utf-8'))

break_time = time.time() - break_time
print(f"获取预测验证码成功\t预测结果为: {Result} \t[{break_time:.3f}s]")
    # print("获取预测验证码成功\t", end='')
