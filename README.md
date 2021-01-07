# WriteFreely API

A [WriteFreely](https://writefreely.org) API client library for Python.

## Install

```
pip install writefreely-py
```

## Quick Start

```
import writefreely as wf

# default WriteFreely instance is 'https://write.as'
c = wf.client(user='foo', password='bar')

# post something to "cool-stuff" collection(blog)
post = c.publish(collection='cool-stuff', body='Hello world!')

print('Visit your new post at:', post['collection']['url'] + post['slug'])
```

Too see what extra parameters some functions accept and response structure, check:
https://developers.write.as/docs/api
