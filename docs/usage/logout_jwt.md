# Logout JWT

!!! note "Prerequisites"

    The creation of JWT tokens will require <a href="https://maxim-f1.github.io/quick_jwt/install/">install</a> and <a href="https://maxim-f1.github.io/quick_jwt/setup/">setup</a> library. 

## Depends job description

Interaction with the library functionality is done through a special `Depends` function that allows you to save the type of data being transferred and perform payload validation of tokens.

To log out of your account, you will need to pass access or refresh tokens to cookies, after which they will be deleted.

## Examples

```python
from quick_jwt import logout_depends

@app.get('/logout-depends')
async def logout_depends_endpoint(logout: logout_depends()):
    return
```