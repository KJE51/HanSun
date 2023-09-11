from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import secure_filename, redirect
import requests
import numpy as np
import cv2
import uuid
import json
import time

bp = Blueprint('function', __name__, url_prefix='/function')


@bp.route('/home', methods = ['POST', 'GET'])
def home():
    url = "http://180.64.249.82:9120/predict"
    if request.method == 'POST':
        
        print(request.files)
        f = request.files['file']
        f.save(secure_filename("old.jpg"))
        files = {
            'image':open("old.jpg", 'rb')
        }
        res = requests.post(url, files=files)
        image1 = np.frombuffer(res.content, dtype=np.uint8)
        image1 = cv2.imdecode(image1, cv2.IMREAD_COLOR)
        cv2.imwrite('main/static/new.png', image1)
        

        path = "main/static/new.png"
        f = [('file', open(path,'rb'))]
        url = 'https://aaguz3sbgl.apigw.ntruss.com/custom/v1/18353/3e9235be8426d15a2758460a365663a7e330221e3fb691996fe7f668f94a68b6/general'
        secret_key = 'aGNDeVNhZll2Q0ZVbHByTkdpVWJOYlVsVUJES1hlVHM='

        request_json = {'images': [{'format': 'png',
                                'name': 'demo'}],
                    'requestId': str(uuid.uuid4()),
                    'version': 'V2',
                    'timestamp': int(round(time.time() * 1000))}
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
 
        headers = {
            'X-OCR-SECRET': secret_key,
        }
 
        response = requests.request("POST", url, headers=headers, data=payload, files=f)
        result = response.json()
        
        ocr_result = ''
        for _ in result['images'][0]['fields']:
            ocr_result = ocr_result + ' ' + _['inferText']
        print(ocr_result)

        global text
        global file
        return render_template('function/text.html', text=ocr_result)
    return render_template('function/home.html')

@bp.route('/text')
def text():
    return render_template('function/text.html')


