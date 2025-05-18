from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from quick_jwt import QuickJWTConfig, logout_depends, QuickJWTMiddleware


def test_logout_depends_cookies():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: logout_depends()):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ.'
        'rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8'
    )
    cookies = [('access', access)]
    client = TestClient(app, cookies=cookies)

    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None
    assert response.cookies.get('access') is None


def test_logout_depends_cookies_invalid():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: logout_depends()):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    access = 'Invalid'
    cookies = [('access', access)]
    client = TestClient(app, cookies=cookies)

    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get('access') is None
