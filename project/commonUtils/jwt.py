import jwt
from datetime import datetime, timedelta
from app.models import Login


def decodeJwt(username, token):
    secretKey = "00000"
    loginObj = Login.objects.filter(username=username)
    if not loginObj:
        resp = {
            "resp_type":"failure",
            "message":"Username not found"
        }
        return resp
    for i in loginObj:
        data = {
            "username":i.username,
            "jwt":i.jwt
        }
    if data['jwt'] != token:
        resp = {
            "resp_type":"failure",
            "message":"Token Mismatch"
        }
        return resp

    try:
        decoded_payload = jwt.decode(token, secretKey, algorithms=['HS256'])
        print("Decoded Payload:", decoded_payload)
        resp = {
            "resp_type":"success",
            "username":decoded_payload['username']
        }
        return resp
    except jwt.ExpiredSignatureError:
        resp = {
            "resp_type":"failure",
            "message":"Token Expired"
        }
        return resp
    except jwt.InvalidTokenError:
        resp = {
            "resp_type":"failure",
            "message":"Invalid Token"
        }
        return resp


def encodeJwt(username):
    secretKey = "00000"
    payload = {
        # "user_id":"123",
        "username":username,
        "exp":datetime.utcnow() + timedelta(minutes=360)
    }
    token = jwt.encode(payload, secretKey, algorithm='HS256')
    return token