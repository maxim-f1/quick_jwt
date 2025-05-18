from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from quick_jwt import QuickJWTConfig, QuickJWTMiddleware
from quick_jwt import (
    access_check_depends,
    refresh_check_depends,
    create_jwt_depends,
    refresh_jwt_depends,
    logout_depends,
    access_check_optional_depends,
    refresh_check_optional_depends,
)

app = FastAPI()
quick_jwt_config = QuickJWTConfig(
    encode_key='key',
    decode_key='key',
)
app.add_middleware(QuickJWTMiddleware, quick_jwt_config)  # noqa


class UserScheme(BaseModel):
    sub: str
    jti: str = Field(default_factory=lambda: str(uuid4()))


@app.get('/create_jwt_depends')
async def create_jwt_depends_endpoint(sub: str, create_jwt: create_jwt_depends(UserScheme, UserScheme)):
    user = UserScheme(sub=sub)
    tokens = await create_jwt.create_jwt_tokens(user, user)
    return tokens


@app.get('/access_check_depends')
async def access_check_depends_endpoint(
    user: access_check_depends(UserScheme),
) -> UserScheme:
    return user


@app.get('/refresh_check_depends')
async def refresh_check_depends_endpoint(user: refresh_check_depends(UserScheme)):
    return user


@app.get('/access_check_depends_and_refresh_check_depends')
async def access_check_depends_and_refresh_check_depends_endpoint(
    access: access_check_depends(UserScheme), refresh: refresh_check_depends(UserScheme)
):
    return access, refresh


@app.get('/access_check_optional_depends')
async def access_check_optional_depends_endpoint(
    user: access_check_optional_depends(UserScheme),
):
    return user


@app.get('/refresh_check_optional_depends')
async def refresh_check_optional_depends_endpoint(
    user: refresh_check_optional_depends(UserScheme),
):
    return user


@app.get('/refresh_jwt_depends')
async def refresh_jwt_depends_endpoint(
    refresh_jwt: refresh_jwt_depends(UserScheme, UserScheme),
):
    access_token = await refresh_jwt.create_access_token(refresh_jwt.payload)
    refresh_token = await refresh_jwt.create_refresh_token(refresh_jwt.payload)
    return {'access': access_token, 'refresh': refresh_token}


@app.get('/logout_depends')
async def logout_depends_endpoint(logout: logout_depends()):
    return


if __name__ == '__main__':
    uvicorn.run('examples.default:app', host='localhost', port=8000, reload=True)
