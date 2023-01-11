from __init__ import app
from .Users import Users
from .Authentication import Auth


# JWT取得及驗證
app.add_route(Auth.as_view(), '/auth')

# 使用者資訊
app.add_route(Users.as_view(), '/users')