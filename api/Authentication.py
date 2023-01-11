from __init__ import app
from sanic.views import HTTPMethodView
from sanic.response import json
import psycopg
import os
import jwt
from datetime import timedelta, datetime, timezone
from sanic_ext import openapi
import bcrypt

class User:
    username: str
    password: str

class Auth(HTTPMethodView):
    @openapi.summary('取得jwt')
    @openapi.description('取得jwt')
    @openapi.tag('帳號、jwt相關功能(auth)')
    @openapi.body({ "application/json": User }, required=True)
    async def post(self, request):
        try:
            username = request.json.get('username')
            password = request.json.get('password')
        except:
            resp = {
                'status': 'success',
                'msg': '請輸入帳號或密碼',
            }
            return json(resp, ensure_ascii=False)

        try:
            async with await psycopg.AsyncConnection.connect(os.getenv('DATABASE_CONFIG')) as conn:
                assert type(username) is str and type(password) is str and username != '' and password != '', '輸入的帳號或密碼格式不符'
                async with conn.cursor() as cursor:
                    await cursor.execute('''
                        SELECT id, username, password, regisration_time FROM users 
                        where username = %(username)s
                    ''' , {
                        'username': username,
                    })
                    row = await cursor.fetchone()
                    assert row != None, '無此帳號!請重新輸入!'
                    salt = row[2][:29].encode('utf-8')
                    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
                    assert hash_pwd == row[2], '密碼輸入錯誤!請重新輸入!'
            tz = timezone(timedelta(hours=+8))
            payload = {
                'id': row[0],
                'username': row[1],
                'exp': datetime.now(tz) + timedelta(hours=3)
            }
            access_token = jwt.encode(payload, os.getenv('SECRET'), algorithm='HS256')

            resp = {
                'status': 'success',
                'msg': 'OK',
                'token': access_token
            }
        except AssertionError as e:
            err_str = str(e)
            resp = {
                'status': 'fail', 
                'msg': err_str 
            }
        finally:
            return json(resp, ensure_ascii=False)

    @openapi.summary('驗證jwt')
    @openapi.description('驗證jwt')
    @openapi.tag('帳號、jwt相關功能(auth)')
    @openapi.secured('token')
    # @openapi.exclude(True)
    async def get(self, request):
        if not request.token:
            resp = {
                'status': 'fail',
                'msg': '請輸入token'
            }
            return json(resp, ensure_ascii=False)
            
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
            return json(resp, ensure_ascii=False)