# WriteFreely

A Python package that wraps the [WriteFreely](https://writefreely.org) API, for use in your Python projects.

## Install

```
pip install writefreely-py
```

## Quick Start

```python
import writefreely as wf

# default WriteFreely instance is 'https://write.as'
c = wf.client(user='foo', password='bar')

# create a post
post = c.create_post(title='Hello World!', body='Hello from **Python**')

print('See your post at: {}/{}'.format(c.host, post['slug']))

# discard current session
c.logout()
```

Too see what extra parameters some functions accept and response structure, check:
https://developers.write.as/docs/api

## Examples

Check the [examples folder](https://github.com/adbenitez/writefreely-py/tree/main/examples) for more code examples.
