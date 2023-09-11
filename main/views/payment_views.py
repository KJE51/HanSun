from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
import requests
from main import db
from main.models import User

bp = Blueprint('payment', __name__, url_prefix='/payment')


@bp.route('/', methods = ['POST', 'GET'])
def payment():
    if request.method == 'POST':
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            'Authorization': "KakaoAK " + "1cb3f6135e11fa98d28aed44ac58920b",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": "TC0ONETIME", 
            "partner_order_id": "1001",  
            "partner_user_id": "testuser",  
            "item_name": "10개", 
            "quantity": 10, 
            "total_amount": 1000, 
            "tax_free_amount": 0,  
            "vat_amount" : 0,
            "approval_url": "http://127.0.0.1:5000/payment/success",
            "cancel_url": "http://127.0.0.1:5000/payment/cancel",
            "fail_url": "http://127.0.0.1:5000/payment/fail",
        }

        res = requests.post(URL, headers=headers, params=params)
        session['payment'] = res.json()['tid']
        #print(res.json()['next_redirect_pc_url'])
        return redirect(res.json()['next_redirect_pc_url'])
    return render_template('payment/payment.html')


@bp.route("/success", methods=['POST', 'GET'])
def sucess():
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "1cb3f6135e11fa98d28aed44ac58920b",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid": session['payment'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",  # 주문번호
        "partner_user_id": "testuser",  # 유저 아이디
        "pg_token": request.args.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    print(res)
    try:
        amount = res.json()['amount']['total']
        context = {
            'res': res,
            'amount': amount,
        }
        user = User.query.filter_by(email=session['email']).first().payNum
        user += 10
        update = User.query.filter_by(email=session['email']).update({"payNum" : user})
        db.session.commit()
    except:
        return redirect(url_for('payment.fail'))
    return render_template('payment/success.html', context=context, res=amount)

@bp.route("/cancel", methods=['POST', 'GET'])
def cancel():
    URL = "https://kapi.kakao.com/v1/payment/order"
    headers = {
        "Authorization": "KakaoAK " + "1cb3f6135e11fa98d28aed44ac58920b",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 가맹점 코드
        "tid": session["payment"],  # 결제 고유 코드

    }

    res = request.post(URL, headers=headers, params=params)
    print(res.text)
    amount = res.json()['cancel_available_amount']['total']

    context = {
        'res': res,
        'cancel_available_amount': amount,
    }
    
    if res.json()['status'] == "QUIT_PAYMENT":
        res = res.json()
        return render_template('payment/cancel.html', params=params, res=res, context=context)


@bp.route("/fail", methods=['POST', 'GET'])
def fail():

    return render_template('payment/fail.html')
