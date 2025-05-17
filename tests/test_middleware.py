import pytest
from fastapi import FastAPI, Request, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

from quick_jwt import QuickJWTConfig, QuickJWTMiddleware


def test_valid_config_definition():
    key = 'New!1 key'
    quick_jwt_config = QuickJWTConfig(
        encode_key=key,
        decode_key=key,
    )

    app = FastAPI()


    @app.get('/')
    def index_endpoint(request: Request):
        return request.state.quick_jwt_config.model_dump(mode='json', exclude={'driver'})  # pragma: no cover

    app.add_middleware(QuickJWTMiddleware, quick_jwt_config)
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    expected_response = {
        'encode_key': key, 'decode_key': key, 'access_token_name': 'access', 'access_token_expires': 'P2D',
        'access_token_path': '/', 'access_token_domain': None, 'access_token_secure': False,
        'access_token_httponly': False, 'access_token_samesite': 'lax', 'refresh_token_name': 'refresh',
        'refresh_token_expires': 'P14D', 'refresh_token_path': '/', 'refresh_token_domain': None,
        'refresh_token_secure': False, 'refresh_token_httponly': False, 'refresh_token_samesite': 'lax',
        'encode_algorithm': 'HS256', 'encode_headers': None, 'encode_json_encoder': None, 'encode_sort_headers': True,
        'decode_algorithms': ['HS256'], 'decode_options': None, 'decode_verify': None, 'decode_detached_payload': None,
        'decode_audience': None, 'decode_subject': None, 'decode_issuer': None, 'decode_leeway': 0.0
    }
    assert response.json() == expected_response


def test_invalid_config_definition():
    app = FastAPI()
    client = TestClient(app)

    @app.get('/')
    def index_endpoint(request: Request):
        return request.state.quick_jwt_config.model_dump(mode='json', exclude={'driver'})  # pragma: no cover

    with pytest.raises(AttributeError) as e:
        client.get('/')
    assert e.value.args[0] == "'State' object has no attribute 'quick_jwt_config'"


def test_invalid_config_type():
    app = FastAPI()
    class ConfigDTO(BaseModel):
        pass  # pragma: no cover
    config = ConfigDTO()
    app.add_middleware(QuickJWTMiddleware, config)

    client = TestClient(app)
    with pytest.raises(Exception) as e:
        client.get('/')
    assert e.value.args[0] == 'Invalid type "config" param in QuickJWTMiddleware'
