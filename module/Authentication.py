from dotenv import load_dotenv
import os
import jwt
from datetime import datetime

load_dotenv()

class Auth:
    def check_jwt(request):
        if not request.token:
            resp = {
                'status': 'fail',
                'msg': '請輸入token'
            }
            return resp
            
        try:
            decode_token = jwt.decode(
                request.token, os.getenv('SECRET'), algorithms=['HS256']
            )
        except jwt.exceptions.InvalidTokenError:
            resp = {
                'status': 'fail',
                'msg': 'token有效期限已過期'
            }
        except:
            resp = {
                'status': 'fail'
            }
        else:  
            resp = {
                'status': 'success',
                'id': decode_token['id'],
                'username': decode_token['username'],
                'exp' : str(datetime.fromtimestamp(decode_token['exp']))
            }
        finally:
            return resp