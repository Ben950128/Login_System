from __init__ import app
from sanic.views import HTTPMethodView
from sanic.response import json
import psycopg
import os
from sanic_ext import openapi
import bcrypt
from psycopg import sql

class User:
    username: str
    password: str

class Users(HTTPMethodView):
    @openapi.summary('使用者註冊')
    @openapi.description('使用者註冊')
    @openapi.tag('使用者資訊(user)')
    @openapi.body({ "application/json": User }, required=True)
    # @openapi.exclude(True)
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
                async with conn.cursor() as cursor:
                    assert type(username) is str and type(password) is str and username != '' and password != '', '輸入的帳號或密碼格式不符'
                    salt = bcrypt.gensalt()
                    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
                    query = sql.SQL('''
                        INSERT INTO users
                            ("username", "password")
                        VALUES 
                            ({username}, {hash_pwd})
                    ''').format(
                        username = sql.Literal(username),
                        hash_pwd = sql.Literal(hash_pwd.decode('utf-8'))
                    )
                    await cursor.execute(query)
                    resp = {
                        'status': 'success',
                        'msg': '註冊成功'
                    }
                    await conn.commit()
        except AssertionError as e:
            err_str = str(e)
            resp = {
                'status': 'fail', 
                'msg': err_str 
            }
        except psycopg.errors.UniqueViolation:
            resp = {
                'status': 'fail', 
                'msg': '帳號已重複，請重新輸入帳號' 
            }
        finally:
            return json(resp, ensure_ascii=False)