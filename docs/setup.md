# Setup

To customize the library, you will need to do a few simple things.

!!! note "Prerequisites"

    Make sure you have installed the library. How to do this was explained on the previous <a href="https://maxim-f1.github.io/quick_jwt/install/">install</a> page.

## Setting variables

To work with Quick JWT, you will need to set up variables in the `QuickJWTConfig` configuration class.

The simplest example of setting up `QuickJWTConfig` that will allow a full user of the library:

```Python
from quick_jwt import QuickJWTConfig

key = "default_key"
config = QuickJWTConfig(encode_key=key, decode_key=key)
```

The __encode_key__ and __decode_key__ variables are the only mandatory arguments in the configuration class.

!!! note tip 

    The `key` variable will be responsible for encrypting and decrypting JWT tokens, as the example will use the `HS256` symmetric encryption algorithm.

!!! note warning "Environment variables"

    This is only a tutorial example. Don't use hardcode in your project. It is better to use `.env` files with environment variables. 
    If the variables are already in the environment, this code will suffice: 

    ```Python 
    from quick_jwt import QuickJWTConfig
    
    config = QuickJWTConfig()
    ```    

    This is possible thanks to the <a href=â€œhttps://docs.pydantic.dev/latest/concepts/pydantic_settings/â€>pydantic_settings</a> library.

## Middleware

In order for Quick JWT to know what variables you have defined for your project you must use `QuickJWTMiddleware`:

```Python
from fastapi import FastAPI
from quick_jwt import (
    QuickJWTConfig,
    QuickJWTMiddleware,
)

key = "default_key"
config = QuickJWTConfig(encode_key=key, decode_key=key)

app = FastAPI()
app.add_middleware(QuickJWTMiddleware, config)
```

Now your project is ready to fully utilize the Quick JWT library

## Advanced settings

Inside the library there is a wide range of functionality for customizing its behavior. The following is a list of the most common ways to override the standard logic.

### PyJWT options

There are cases when it is necessary to strictly specify which fields will be used in access and refresh tokens. You can override the driver for this purpose:

```Python
from jwt import PyJWT
from quick_jwt import QuickJWTConfig

options = {
    "verify_signature": True,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iat": False,
    "verify_aud": False,
    "verify_iss": False,
    "verify_sub": True,
    "verify_jti": False,
    "require": [],
}
driver = PyJWT(
    options=options
)
config = QuickJWTConfig(driver=driver)
```

### Cookie parameters for access and refresh tokens

```Python
from datetime import timedelta

from quick_jwt import QuickJWTConfig

config = QuickJWTConfig(
    access_token_name='access',
    access_token_expires=timedelta(days=2),
    access_token_path='/',
    access_token_domain='domain.com',
    access_token_secure=True,
    access_token_httponly=True,
    access_token_samesite='lax',
)
```

!!! note tip

    You can override the refresh behavior of the token by the same principle.

### Additional variables for the encode function

When encrypting tokens, additional parameters can be thrown in:

```Python
import json

from quick_jwt import QuickJWTConfig

config = QuickJWTConfig(
    encode_algorithm='HS256',
    encode_headers={'X-Custom-Header': 'Value'},
    encode_json_encoder=json.JSONEncoder,
    encode_sort_headers=False,
)
```

### Additional variables for the decode function

```Python
from quick_jwt import QuickJWTConfig

config = QuickJWTConfig(
    decode_algorithms=['HS256'],
    decode_options={'sub': False},
    decode_verify=False,
)
```

### Custom driver

The default driver for the library is <a href=â€œhttps://pyjwt.readthedocs.ioâ€>PyJWT</a>, but you can also override it with the `driver` variable:

```Python
from quick_jwt import QuickJWTConfig
    
config = QuickJWTConfig(driver=AnotherDriver())
```

!!! note tip

    For a custom driver to work correctly, it must have `encode` and `decode` functions.
