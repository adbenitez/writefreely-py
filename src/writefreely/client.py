"""WriteFreely API client.
"""
from json import JSONDecodeError
from typing import Callable, List, Optional, Union

import requests


class Client:
    def __init__(self, host: str) -> None:
        """WriteFreely client class."""
        self.host = host.strip('/')
        self.token: Optional[str] = None

    def _request(self, action: Callable, endpoint: str,
                 data: Union[dict, list] = None,
                 headers: dict = {}) -> Union[dict, list, None]:
        headers['Content-Type'] = 'application/json'
        if self.token:
            headers['Authorization'] = 'Token {}'.format(self.token)
        with action(self.host + endpoint, json=data, headers=headers) as resp:
            resp.raise_for_status()
            if resp.text:
                return resp.json()['data']
            return None

    def _get(self, endpoint: str, data: Union[dict, list] = None, headers: dict = {}) -> Union[dict, list]:
        return self._request(requests.get, endpoint, data, headers)

    def _post(self, endpoint: str, data: Union[dict, list] = None, headers: dict = {}) -> Union[dict, list]:
        return self._request(requests.post, endpoint, data, headers)

    def _delete(self, endpoint: str, data: Union[dict, list] = None, headers: dict = {}) -> Union[dict, list]:
        return self._request(requests.delete, endpoint, data, headers)

    # ===== ACCOUNT =====

    def login(self, user: str, password: str) -> dict:
        """Authenticate with the WriteFreely instance."""
        data: dict = self._post(
            '/api/auth/login', {'alias': user, 'pass': password})
        self.token = data['access_token']
        return data

    def logout(self) -> dict:
        """Log out of the WriteFreely instance.
        
        Un-authenticates a user with Write.as, permanently invalidating
        the access token used with the request."""
        data = self._delete('/api/auth/me')
        self.token = None
        return data

    def me(self) -> None:
        """Return an authenticated user's basic data."""
        return self._get('/api/me')

    # ===== POSTS =====

    def create_post(self, body: str, collection: str = None, **kwargs) -> dict:
        """Publish a post.
        
        This creates a new post, associating it with a user account if
        authenticated. If collection is given, post will be published in
        that collection.
        """
        if collection:
            endpoint = '/api/collections/{}/posts'.format(collection)
        else:
            endpoint = '/api/posts'
        return self._post(endpoint, {'body': body, **kwargs})

    def get_post(self, post_id_or_slug: str, collection: str = None) -> dict:
        """Retrieve a post by id, or a collection post by slug if collection is given."""
        if collection:
            return self._get('/api/collections/{}/posts/{}'.format(
                collection, post_id_or_slug))
        return self._get('/api/posts/' + post_id_or_slug)

    def get_posts(self, collection: str = None) -> dict:
        """Retrieve all posts, or posts from the given collection."""
        if collection:
            return self._get(
                '/api/collections/{}/posts'.format(collection))
        return self._get('/api/me/posts')

    def update_post(self, post_id: str, body: str, **kwargs) -> dict:
        """Update an existing post."""
        return self._post('/api/posts/' + post_id, {'body': body, **kwargs})

    def delete_post(self, post_id: str) -> dict:
        """Delete a post."""
        return self._delete('/api/posts/' + post_id)

    def claim_post(self, post_id: str, post_token: str,
                   collection: str = None) -> dict:
        """Add unowned post to the user/account. If collection is given,
        then add post to the collection.
        """
        return self.claim_posts(
            [{'id': post_id, 'token': post_token}], collection)

    def claim_posts(self, posts: List[dict], collection: str = None) -> dict:
        """Add unowned posts to user/account. If collection is given,
        then add the group of posts to the collection.
        """
        if collection:
            return self._post('/api/collections/{}/collect'.format(collection), posts)
        return self._post('/api/posts/claim', posts)

    def pin_post(self, post_id: str, post_position: int,
                 collection: str) -> dict:
        """Pin a post to a collection.
        
        Pinned posts will show up as a navigation items in the 
        collection/blog home page header, instead of on the blog itself.
        """
        return self.pin_posts(
            [{'id': post_id, 'position': post_position}], collection)

    def pin_posts(self, posts: List[dict], collection: str) -> dict:
        """Pin posts to a collection.
        
        Pinned posts will show up as a navigation items in the 
        collection/blog home page header, instead of on the blog itself.
        """
        return self._post('/api/collections/{}/pin'.format(collection), posts)
        
    def unpin_post(self, post_id: str, collection: str) -> dict:
        """Unpin a post from a collection."""
        return self.unpin_posts([{'id': post_id}], collection)

    def unpin_posts(self, posts: List[dict], collection: str) -> dict:
        """Unpin posts from a collection."""
        return self._post('/api/collections/{}/unpin'.format(collection), posts)

    # ===== COLLECTIONS =====

    def create_collection(self, alias: str = None, title: str = None) -> dict:
        """Create a new collection."""
        assert alias or title, 'Alias or title should be supplied.'
        return self._post(
            '/api/collections', {'alias': alias, 'title': title})

    def get_collection(self, alias: str) -> dict:
        """Get a collection by alias."""
        return self._get('/api/collections/' + alias)

    def get_collections(self) -> List[dict]:
        """Get collections list."""
        return self._get('/api/me/collections')

    def update_collection(self, alias: str, **kwargs) -> dict:
        """Update attributes of an existing collection.

        Supply only the fields you would like to update. Any fields left
        out will remain unchanged.
        """
        return self._post('/api/collections/' + alias, kwargs)

    def delete_collection(self, alias: str) -> dict:
        """Delete a collection.

        This permanently deletes a collection and makes any posts on it
        anonymous.
        """
        return self._delete('/api/collections/' + alias)

    def get_channels(self) -> dict:
        """Return an array of the authenticated user's connected channels, or integrations.

        For channels that aren't a centralized service, like Mastodon,
        you'll also see a url property of the specific instance or host
        that the user has connected to.
        """
        return self._get('/api/me/channels')
