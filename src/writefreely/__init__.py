from pkg_resources import DistributionNotFound, get_distribution

from .client import Client

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "0.0.0.dev0-unknown"


def client(
    host: str = "https://write.as",
    user: str = None,
    password: str = None,
    token: str = None,
) -> Client:
    c = Client(host)
    if token:
        c.token = token
    elif user and password:
        c.login(user, password)
    return c
