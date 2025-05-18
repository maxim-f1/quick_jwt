from uuid import UUID

from fastapi import FastAPI, status
from pydantic import BaseModel
from starlette.testclient import TestClient

from quick_jwt import QuickJWTConfig, access_check_optional_depends, QuickJWTMiddleware


def test_access_check_optional_depends():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: access_check_optional_depends(Payload)):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ.'
        'rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8'
    )
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = client.get('/', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'sub': sub}


def test_access_check_optional_depends_invalid_token():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: access_check_optional_depends(Payload)):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ.'
        'rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8'
    )
    headers = {
        'Authorization': f'Invalid {access}'
    }
    response = client.get('/', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


def test_access_check_optional_depends_invalid_bearer():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: access_check_optional_depends(Payload)):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    access = (
        'invalid_token'
    )
    headers = {
        'Authorization': f'Bearer {access}'
    }
    response = client.get('/', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


def test_access_check_optional_depends_cookies():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: access_check_optional_depends(Payload)):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ.'
        'rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8'
    )
    cookies = [
        ('access', access)
    ]
    client = TestClient(app, cookies=cookies)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'

    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'sub': sub}


def test_access_check_optional_depends_invalid_token_cookies():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(payload: access_check_optional_depends(Payload)):
        return payload  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    access = (
        'invalid_token'
    )
    cookies = [
        ('access', access)
    ]
    client = TestClient(app, cookies=cookies)

    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None
