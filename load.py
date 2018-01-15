import os

"""Safe load for environment variables. Raises ValueError if variable is missing."""
def load_env_var(var):
    v = os.environ.get(var, None)
    if not v:
        raise ValueError('You must have "{}" variable'.format(var))
    return v
