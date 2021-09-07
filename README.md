# WriteFreely

[![Latest Release](https://img.shields.io/pypi/v/writefreely-py.svg)](https://pypi.org/project/writefreely-py)
[![Supported Versions](https://img.shields.io/pypi/pyversions/writefreely-py.svg)](https://pypi.org/project/writefreely-py)
[![Downloads](https://pepy.tech/badge/writefreely-py)](https://pepy.tech/project/writefreely-py)
[![License](https://img.shields.io/pypi/l/writefreely-py.svg)](https://pypi.org/project/writefreely-py)
[![CI](https://github.com/adbenitez/writefreely-py/actions/workflows/python-ci.yml/badge.svg)](https://github.com/adbenitez/writefreely-py/actions/workflows/python-ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python package that wraps the [WriteFreely](https://writefreely.org) API, for use in your Python projects.

## Install

```
pip install writefreely-py
```

## Quick Start

```python
import writefreely as wf

# default WriteFreely instance is "https://write.as"
c = wf.client(user="foo", password="bar")

# create a post
post = c.create_post(title="Hello World!", body="Hello from **Python**")

print(f"See your post at: {c.host}/{post['slug']}")

# discard current session
c.logout()
```

Too see what extra parameters some functions accept and response structure, check:
https://developers.write.as/docs/api/

## Examples

Check the [examples folder](https://github.com/adbenitez/writefreely-py/tree/main/examples) for more code examples.
