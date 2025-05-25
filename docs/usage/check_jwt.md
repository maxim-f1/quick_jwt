# Check JWT

!!! note "Prerequisites"

    The creation of JWT tokens will require <a href="https://maxim-f1.github.io/quick_jwt/install/">install</a> and <a href="https://maxim-f1.github.io/quick_jwt/setup/">setup</a> library. 

## Depends job description

Interaction with the library functionality is done through a special `Depends` function that allows you to save the type of data being transferred and perform payload validation of tokens.

## Examples

### Access token

To check the access token you need to use the function `check_jwt_depends`

```python
from pydantic import BaseModel
from quick_jwt import (
    access_check_depends
)

class UserScheme(BaseModel):
    sub: str

    
@app.get("/access-token-check")
async def access_token_check(
        user: access_check_depends(UserScheme)
) -> UserScheme:
    return user
```

!!! note "What happened?"

    The `access_check_depends` function was passed a scheme into which the `access` token payload will be converted. Also, a field for sending the token via headers or cookies appeared in the endpoint.

### Refresh token

In addition to checking the access token, you can also check the refresh token:

```python
from pydantic import BaseModel
from quick_jwt import (
    refresh_check_depends
)

class UserScheme(BaseModel):
    sub: str

    
@app.get("/refresh-token-check")
async def refresh_token_check(
        user: refresh_check_depends(UserScheme)
) -> UserScheme:
    return user
```

!!! note "What happened?"

    The `refresh_check_depends` function was passed a scheme into which the `refresh` token payload will be converted. Also, a field for sending the token via headers or cookies appeared in the endpoint.
