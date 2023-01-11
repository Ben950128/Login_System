from sanic import Sanic
from sanic_ext import Extend
from dotenv import load_dotenv

app = Sanic(__name__)
Extend(app)
app.config
# app.config['API_SCHEMES'] = ['https']
# app.config['API_HOST'] = 'api.irmp.tw'
# app.config['API_BASEPATH'] = 'taipei-geo'
# app.config['API_TITLE'] = '測站觀測資料-API'
# app.config['OAS_URL_PREFIX'] = '/taipei-geo/docs'
app.ext.openapi.add_security_scheme(
    'token',
    'http',
    scheme='bearer',
    bearer_format='JWT'
)
load_dotenv()

# import api時會回來import此__init__.py，此時並不再重新讀取此__init__.py，會依照之前讀取的內容抓取，因此必須要先有app再import api
import api