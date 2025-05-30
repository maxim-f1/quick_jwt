from datetime import timedelta
from uuid import UUID

import pytest
from fastapi import FastAPI
from httpx import QueryParams
from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.testclient import TestClient

from quick_jwt import QuickJWTConfig, create_jwt_depends, QuickJWTMiddleware


def test_create_jwt_depends_create_access_token():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        return await create_jwt.create_access_token(Payload(sub=sub))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'
    response = client.get('/', params=QueryParams(sub=sub))
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ.'
        'rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == access
    assert response.cookies.get('access') == access


def test_create_jwt_depends_create_refresh_token():
    key = '8296734789620'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class Payload(BaseModel):
        sub: UUID
        jti: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, jti: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        return await create_jwt.create_refresh_token(Payload(sub=sub, jti=jti))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = 'bb025fa9-73b8-470a-abfc-e337cbcc2d5f'
    jti = '75446dc0-f07a-4614-8e2a-6ba90857d8b3'
    response = client.get('/', params=QueryParams(sub=sub, jti=jti))
    refresh = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiJiYjAyNWZhOS03M2I4LTQ3MGEtYWJmYy1lMzM3Y'
        '2JjYzJkNWYiLCJqdGkiOiI3NTQ0NmRjMC1mMDdhLTQ2MTQtOGUyYS02YmE5MDg1N2Q4YjMifQ.'
        'ZKW8_9GAIzxNYB_jF26486ez0ZueuASCO6-oIOF8CE0'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == refresh
    assert response.cookies.get('refresh') == refresh


def test_create_jwt_depends_create_jwt_tokens():
    key = ' '
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        payload = Payload(sub=sub)
        return await create_jwt.create_jwt_tokens(payload, payload)  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '988f1c87-d9df-4d16-8f05-f6278ad9abf1'
    response = client.get('/', params=QueryParams(sub=sub))
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI5ODhmMWM4Ny1kOWRmLTRkMTYtOGYwNS1mNjI3OGFkOWFiZjEifQ.'
        '2HDe99YW4j78VtffiIXEUvSwvaU6s-5Moa3e5ZPBSzM'
    )
    refresh = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI5ODhmMWM4Ny1kOWRmLTRkMTYtOGYwNS1mNjI3OGFkOWFiZjEifQ.'
        '2HDe99YW4j78VtffiIXEUvSwvaU6s-5Moa3e5ZPBSzM'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'access': access, 'refresh': refresh}
    assert response.cookies.get('access') == access
    assert response.cookies.get('refresh') == refresh


def test_create_jwt_depends_create_access_token_invalid_scheme():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class Payload(BaseModel):
        sub: UUID

    class Invalid(BaseModel):
        jti: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        return await create_jwt.create_access_token(Invalid(jti=sub))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'
    with pytest.raises(ValidationError) as e:
        client.get('/', params=QueryParams(sub=sub))
    assert e.value.json() == (
        '[{"type":"model_type","loc":[],"msg":"Input should be a valid dictionary or instance of Payload",'
        '"input":{"jti":"73031704-0799-4c4e-8689-3b91d35c2d18"},"ctx":{"class_name":"Payload"},'
        '"url":"https://errors.pydantic.dev/2.11/v/model_type"}]'
    )


def test_create_jwt_depends_create_refresh_token_invalid_scheme():
    key = 'Some1! Key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class Payload(BaseModel):
        sub: UUID

    class Invalid(BaseModel):
        jti: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        return await create_jwt.create_refresh_token(Invalid(jti=sub))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'
    with pytest.raises(ValidationError) as e:
        client.get('/', params=QueryParams(sub=sub))
    assert e.value.json() == (
        '[{"type":"model_type","loc":[],"msg":"Input should be a valid dictionary or instance of Payload",'
        '"input":{"jti":"73031704-0799-4c4e-8689-3b91d35c2d18"},"ctx":{"class_name":"Payload"},'
        '"url":"https://errors.pydantic.dev/2.11/v/model_type"}]'
    )


def test_create_jwt_depends_with_custom_expiration():
    key = 'custom_exp_key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
        access_token_expires=timedelta(seconds=10),
        refresh_token_expires=timedelta(seconds=30),
    )

    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        payload = Payload(sub=sub)
        return await create_jwt.create_jwt_tokens(payload, payload)  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '988f1c87-d9df-4d16-8f05-f6278ad9abf1'
    response = client.get('/', params=QueryParams(sub=sub))

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.json()
    assert 'refresh' in response.json()
    assert response.cookies.get('access') is not None
    assert response.cookies.get('refresh') is not None


def test_create_jwt_depends_with_different_payload_types():
    key = 'different_payloads_key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class AccessPayload(BaseModel):
        sub: UUID
        name: str

    class RefreshPayload(BaseModel):
        sub: UUID
        jti: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(
        sub: UUID,
        name: str,
        jti: UUID,
        create_jwt: create_jwt_depends(AccessPayload, RefreshPayload),
    ):
        access_payload = AccessPayload(sub=sub, name=name)
        refresh_payload = RefreshPayload(sub=sub, jti=jti)
        return await create_jwt.create_jwt_tokens(access_payload, refresh_payload)  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '988f1c87-d9df-4d16-8f05-f6278ad9abf1'
    name = 'test_user'
    jti = '75446dc0-f07a-4614-8e2a-6ba90857d8b3'
    response = client.get('/', params=QueryParams(sub=sub, name=name, jti=jti))

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.json()
    assert 'refresh' in response.json()
    assert response.cookies.get('access') is not None
    assert response.cookies.get('refresh') is not None


def test_create_jwt_depends_with_additional_claims():
    key = 'additional_claims_key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    class Payload(BaseModel):
        sub: UUID
        role: str

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, role: str, create_jwt: create_jwt_depends(Payload, Payload)):
        payload = Payload(sub=sub, role=role)
        return await create_jwt.create_access_token(payload)  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'
    role = 'admin'
    response = client.get('/', params=QueryParams(sub=sub, role=role))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None
    assert response.cookies.get('access') is not None


def test_create_jwt_depends_create_access_token_access_expired():
    key = ''
    quick_jwt_config = QuickJWTConfig(encode_key=key, decode_key=key, access_token_expires=timedelta(seconds=1))

    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get('/')
    async def endpoint(sub: UUID, create_jwt: create_jwt_depends(Payload, Payload)):
        return await create_jwt.create_access_token(Payload(sub=sub))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = '73031704-0799-4c4e-8689-3b91d35c2d18'
    response = client.get('/', params=QueryParams(sub=sub))
    access = (
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
        'eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ.'
        'NGGqPBwgssOqSVhbMj5rQznZ-VLQ99lXT6KcOILWloM'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == access
    assert response.cookies.get('access') == access
