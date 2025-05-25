# Refresh JWT

!!! note "Prerequisites"

    The creation of JWT tokens will require <a href="https://maxim-f1.github.io/quick_jwt/install/">install</a> and <a href="https://maxim-f1.github.io/quick_jwt/setup/">setup</a> library. 

## Depends job description

Interaction with the library functionality is done through a special `Depends` function that allows you to save the type of data being transferred and perform payload validation of tokens.

To update the token, the user must pass the refresh token into the request via headers or cookies.

After checking the token, a pair of new JWT tokens will be created.

## Examples

### Base example

```python
from pydantic import BaseModel
from quick_jwt import (
    refresh_jwt_depends
)

class UserScheme(BaseModel):
    sub: str


@app.get('/refresh-jwt')
async def refresh_jwt_depends_endpoint(
    refresh_jwt: refresh_jwt_depends(UserScheme, UserScheme),
):
    access_token = await refresh_jwt.create_access_token(refresh_jwt.payload)
    refresh_token = await refresh_jwt.create_refresh_token(refresh_jwt.payload)
    return {'access': access_token, 'refresh': refresh_token}
```

!!! note "What happened?"

    At the start of the `refresh_jwt_depends` function, the token was checked. If it was valid for the user, a pair of JWT tokens is created
