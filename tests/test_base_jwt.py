import pytest
from starlette.requests import Request

from quick_jwt.core.abc import BaseJWT


class Children(BaseJWT):
    def without_request(self):
        self._get_config_from_request()

    def config_not_found(self):
        self._request = Request
        self._get_config_from_request()

    def some_args_is_none(self, request, response, config):
        self._request = request
        self._response = response
        self._config = config
        self._get_config()
        self._get_request()
        self._get_response()


def test_base_jwt_reqeust_not_found():
    with pytest.raises(AttributeError) as e:
        Children().without_request()

    assert e.value.args[0] == '_reqeust field not found'


def test_base_jwt_config_not_found():
    with pytest.raises(Exception):
        Children().config_not_found()


@pytest.mark.parametrize('_request', [None, 1])
@pytest.mark.parametrize('response', [None, 1])
@pytest.mark.parametrize('config', [None, 1])
def test_base_jwt_config_some_args_is_none(_request, response, config):
    if _request is not None and response is not None and config is not None:
        assert Children().some_args_is_none(_request, response, config) is None
    else:
        with pytest.raises(Exception) as e:
            Children().some_args_is_none(_request, response, config)

        assert e.value.args[0] == 'The __call__ function was not called.'
