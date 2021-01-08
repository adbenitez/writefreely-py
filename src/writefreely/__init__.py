
from .client import Client

__version__ = '1.0.0'


def client(host: str = 'https://write.as', user: str = None,
           password: str = None, token: str = None) -> Client:
    c = Client(host)
    if token:
        c.token = token
    elif user and password:
        c.login(user, password)
    return c
