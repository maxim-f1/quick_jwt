# Create JWT

!!! note "Prerequisites"

    The creation of JWT tokens will require <a href="https://maxim-f1.github.io/quick_jwt/install/">install</a> and <a href="https://maxim-f1.github.io/quick_jwt/setup/">setup</a> library. 

## Depends job description

Interaction with the library functionality is done through a special `Depends` function that allows you to save the type of data being transferred and perform payload validation of tokens.

## Examples

### Basic use case

To create tokens, you need to add an annotation to the endpoint:

```Python
from pydantic import BaseModel
from quick_jwt import (
    JWTTokensDTO,
    create_jwt_depends
)

class UserScheme(BaseModel):
    sub: str

    
@app.get("/create-tokens")
async def create_tokens(
        sub: str,
        jwt: create_jwt_depends(
            access_payload=UserScheme, 
            refresh_payload=UserScheme
        )
) -> JWTTokensDTO:
    user = UserScheme(sub=sub)
    tokens = await jwt.create_jwt_tokens(
        access_payload=user, 
        refresh_payload=user
    )
    return tokens
```

!!! note "What happened?"

    An instance class that has a `create_jwt_tokens` function to generate tokens was written to the `jwt` variable. The `payload` schemas for `access` and `refresh` tokens were passed into the parameters of the `create_jwt_depends` function. The `create_jwt_tokens` function parameters were passed to the `create_jwt_tokens` function to be converted into payloads and packaged into JWT tokens.

!!! note tip

    In our case, the patterns for `access` and `refresh` tokens are the same to simplify the examples. You can use different patterns.

A pair of tokens will be returned in response to this request:

```json  title="Response"
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lX2lkIn0.EerZU4uZCRh7yXxOqsZKTwzls7BnL-6C8jidTTkit6k",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lX2lkIn0.EerZU4uZCRh7yXxOqsZKTwzls7BnL-6C8jidTTkit6k"
}
```

### Generating access token

If you only need to create `access` or `refresh` you can call the `create_access_token` or `create_refresh_token` function respectively.

```Python
from pydantic import BaseModel
from quick_jwt import create_jwt_depends

class UserScheme(BaseModel):
    sub: str

    
@app.get("/create-access-token")
async def create_access_token(
        sub: str,
        jwt: create_jwt_depends(
            access_payload=UserScheme, 
            refresh_payload=UserScheme
        )
) -> str:
    user = UserScheme(sub=sub)
    token = await jwt.create_access_token(
        access_payload=user
    )
    return token
```

!!! note

    The function generated an `access` token that can be used in further checks.

```json title="Response"
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lX2lkIn0.EerZU4uZCRh7yXxOqsZKTwzls7BnL-6C8jidTTkit6k"
```

### Generating refresh token

```Python
from pydantic import BaseModel
from quick_jwt import create_jwt_depends

class UserScheme(BaseModel):
    sub: str

    
@app.get("/create-refresh-token")
async def create_refresh_token(
        sub: str,
        jwt: create_jwt_depends(
            access_payload=UserScheme, 
            refresh_payload=UserScheme
        )
) -> str:
    user = UserScheme(sub=sub)
    token = await jwt.create_refresh_token(
        refresh_payload=user
    )
    return token
```

!!! note

    The function generated a `refresh` token that can be used in further checks.

```json title="Response"
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lX2lkIn0.EerZU4uZCRh7yXxOqsZKTwzls7BnL-6C8jidTTkit6k"
```
