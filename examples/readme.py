import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from quick_jwt import (
    QuickJWTConfig,
    QuickJWTMiddleware,
    create_jwt_depends,
)

key = "default_key"
quick_jwt_config = QuickJWTConfig(encode_key=key, decode_key=key)

app = FastAPI()
app.add_middleware(QuickJWTMiddleware, quick_jwt_config)


class UserScheme(BaseModel):
    sub: str


@app.get("/create-tokens")
async def create_tokens(
        sub: str,
        jwt: create_jwt_depends(UserScheme, UserScheme)
):
    user = UserScheme(sub=sub)
    tokens = await jwt.create_jwt_tokens(user, user)
    return tokens


if __name__ == '__main__':
    uvicorn.run('examples.readme:app', host='localhost', port=8000, reload=True)
