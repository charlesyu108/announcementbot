import functools
from flask import request, Response

"""Function checks provided username and password against those stored
in creds (dictionary-like object). """
def check_auth(username, password, creds):
    return username == creds['username'] and password == creds['password']

"""Sends a 401 response that enables basic auth."""
def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

"""Decorator function to prompt and verify authentication.
Note: If f is not provided, returns a partial application of requires_auth with
creds parameter filled in."""
def requires_auth(f = None, creds={'username':'', 'password':''}):
    if f is None:
        return functools.partial(requires_auth, creds = creds)
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password, creds):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
