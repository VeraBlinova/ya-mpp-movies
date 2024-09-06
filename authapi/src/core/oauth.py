import os

from social_core.backends.yandex import YaruOAuth2

from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config


oauth2_config = OAuth2Config(
    allow_http=True,
    jwt_secret=os.getenv("AUTHJWT_SECRET_KEY",'WowSoSecret'),
    jwt_expires=os.getenv("AUTHJWT_ACCESS_EXPIRES",900),
    jwt_algorithm=os.getenv("JWT_ALGORITHM",'HS256'),
    clients=[
        OAuth2Client(
            backend=YaruOAuth2,
            redirect_uri=os.getenv("OAUTH_REDIRECT_URI",'http://127.0.0.1/authapi/api/v1/oauth'),
            client_id=os.getenv("OAUTH2_YANDEX_CLIENT_ID",'27cd5f7112894a3184fa8e666ad28c5b'),
            client_secret=os.getenv("OAUTH2_YANDEX_CLIENT_SECRET",'9a2c5db4a7da4d4fb8ebfde5a7907e23'),
        )
    ]
)
