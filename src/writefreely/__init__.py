
from .client import Client

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "0.0.0.dev0-unknown"


def client(host: str = 'https://write.as', user: str = None,
           password: str = None, token: str = None) -> Client:
    c = Client(host)
    if token:
        c.token = token
    elif user and password:
        c.login(user, password)
    return c
