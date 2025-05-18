from uuid import UUID

import pytest
from fastapi import FastAPI
from httpx import QueryParams
from pydantic import BaseModel
from starlette import status
from starlette.testclient import TestClient

from quick_jwt import refresh_jwt_depends, QuickJWTConfig, QuickJWTMiddleware


def test_refresh_jwt_depends_create_access_token():
    key = "Some1! Key"
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get("/")
    async def endpoint(sub: UUID, refresh_jwt: refresh_jwt_depends(Payload, Payload)):
        return await refresh_jwt.create_access_token(Payload(sub=sub))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = "73031704-0799-4c4e-8689-3b91d35c2d18"
    refresh = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ."
        "rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8"
    )
    headers = {
        "Authorization": f"Bearer {refresh}"
    }
    response = client.get("/", params=QueryParams(sub=sub), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == refresh
    assert response.cookies.get("access") == refresh


def test_refresh_jwt_depends_create_refresh_token():
    key = "8296734789620"
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID
        jti: UUID

    app = FastAPI()

    @app.get("/")
    async def endpoint(sub: UUID, jti: UUID, refresh_jwt: refresh_jwt_depends(Payload, Payload)):
        return await refresh_jwt.create_refresh_token(Payload(sub=sub, jti=jti))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    sub = "bb025fa9-73b8-470a-abfc-e337cbcc2d5f"
    jti = "75446dc0-f07a-4614-8e2a-6ba90857d8b3"

    refresh = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJiYjAyNWZhOS03M2I4LTQ3MGEtYWJmYy1lMzM3Y"
        "2JjYzJkNWYiLCJqdGkiOiI3NTQ0NmRjMC1mMDdhLTQ2MTQtOGUyYS02YmE5MDg1N2Q4YjMifQ."
        "ZKW8_9GAIzxNYB_jF26486ez0ZueuASCO6-oIOF8CE0"
    )
    headers = {
        "Authorization": f"Bearer {refresh}"
    }

    response = client.get("/", params=QueryParams(sub=sub, jti=jti), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None
    assert response.cookies.get("refresh") is not None


def test_refresh_jwt_depends_create_access_token_cookies():
    key = "Some1! Key"
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()

    @app.get("/")
    async def endpoint(sub: UUID, refresh_jwt: refresh_jwt_depends(Payload, Payload)):
        return await refresh_jwt.create_access_token(Payload(sub=sub))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    refresh = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ."
        "rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8"
    )
    cookies = {
        "refresh": refresh
    }
    client = TestClient(app, cookies=cookies)
    sub = "73031704-0799-4c4e-8689-3b91d35c2d18"
    response = client.get("/", params=QueryParams(sub=sub))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == refresh
    assert response.cookies.get("access") == refresh


def test_refresh_jwt_depends_create_refresh_token_cookies():
    key = "8296734789620"
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )
    class Payload(BaseModel):
        sub: UUID
        jti: UUID

    app = FastAPI()

    @app.get("/")
    async def endpoint(sub: UUID, jti: UUID, refresh_jwt: refresh_jwt_depends(Payload, Payload)):
        return await refresh_jwt.create_refresh_token(Payload(sub=sub, jti=jti))  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    refresh = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJiYjAyNWZhOS03M2I4LTQ3MGEtYWJmYy1lMzM3Y"
        "2JjYzJkNWYiLCJqdGkiOiI3NTQ0NmRjMC1mMDdhLTQ2MTQtOGUyYS02YmE5MDg1N2Q4YjMifQ."
        "ZKW8_9GAIzxNYB_jF26486ez0ZueuASCO6-oIOF8CE0"
    )
    cookies = {
        "refresh": refresh
    }
    client = TestClient(app, cookies=cookies)
    sub = "bb025fa9-73b8-470a-abfc-e337cbcc2d5f"
    jti = "75446dc0-f07a-4614-8e2a-6ba90857d8b3"

    response = client.get("/", params=QueryParams(sub=sub, jti=jti))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None
    assert response.cookies.get("refresh") is not None


def test_access_check_depends__validate_driver():
    key = "Some1! Key"
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
        driver=None
    )
    class Payload(BaseModel):
        sub: UUID

    app = FastAPI()
    sub = "bb025fa9-73b8-470a-abfc-e337cbcc2d5f"
    @app.get("/")
    async def endpoint(refresh_jwt: refresh_jwt_depends(Payload, Payload)):
        payload = Payload(  # pragma: no cover
            sub=sub
        )
        return refresh_jwt.create_jwt_tokens(payload, payload)  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    refresh = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiI3MzAzMTcwNC0wNzk5LTRjNGUtODY4OS0zYjkxZDM1YzJkMTgifQ."
        "rs-zlSQ6wuNFQY7Unpt02iM1qNCqOc1uYu42F-VuAz8"
    )
    headers = {
        "Authorization": f"Bearer {refresh}"
    }


    with pytest.raises(Exception):
        client.get("/", headers=headers)
