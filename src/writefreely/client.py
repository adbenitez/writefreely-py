"""WriteFreely API client.
"""
from typing import Callable, List, Optional, Union

import requests


class Client:
    def __init__(self, host: str) -> None:
        """WriteFreely client class."""
        host = host.strip('/')
        if host.startswith(('https://', 'http://')):
            self.host = host
        else:
            self.host = 'https://' + host
        self.token: Optional[str] = None

    def _request(self, action: Callable, endpoint: str,
                 data: Union[dict, list] = None,
                 headers: dict = None,
                 needs_auth: bool = True):
        headers = headers or dict()
        headers['Content-Type'] = 'application/json'
        if needs_auth:
            if not self.is_authenticated():
                raise ValueError('Authentication needed.')
            headers['Authorization'] = 'Token {}'.format(self.token)
        with action(self.host + endpoint, json=data, headers=headers) as resp:
            resp.raise_for_status()
            if resp.text:
                return resp.json()['data']

    def _get(self, endpoint: str, **kwargs):
        return self._request(requests.get, endpoint, **kwargs)

    def _post(self, endpoint: str, **kwargs):
        return self._request(requests.post, endpoint, **kwargs)

    def _delete(self, endpoint: str, **kwargs):
        return self._request(requests.delete, endpoint, **kwargs)

    # ===== ACCOUNT =====

    def login(self, user: str, password: str) -> dict:
        """Authenticate a user with the WriteFreely instance.

        An access token is created for future authenticated requests.
        Users can only authenticate with their primary account, i.e. the
        first collection/blog they created, which may or may not have
        multiple collections associated with it.
        """
        data = self._post(
            '/api/auth/login',
            data={'alias': user, 'pass': password},
            needs_auth=False,
        )
        self.token = data['access_token']
        return data

    def logout(self) -> None:
        """Log out of the WriteFreely instance.

        Un-authenticates a user with WriteFreely, permanently invalidating
        the access token used with the request.
        """
        self._delete('/api/auth/me', needs_auth=True)
        self.token = None

    def me(self) -> dict:
        """Retrieve authenticated user.

        Returns an authenticated user's basic data.
        """
        return self._get('/api/me', needs_auth=True)

    def is_authenticated(self) -> bool:
        """Return True account is logged in, False otherwise."""
        return bool(self.token)

    # ===== POSTS =====

    def create_post(self, body: str, collection: str = None, **kwargs) -> dict:
        """Publish a post.

        This creates a new post, associating it with a user account if
        authenticated. If collection is given, post will be published in
        that collection.
        """
        if collection:
            return self._post(
                '/api/collections/{}/posts'.format(collection),
                data={'body': body, **kwargs},
                needs_auth=True,
            )
        return self._post(
            '/api/posts',
            data={'body': body, **kwargs},
            needs_auth=self.is_authenticated(),
        )

    def get_post(self, post_id_or_slug: str, collection: str = None) -> dict:
        """Retrieve a post by id, or a collection post by slug if collection is given.

        This includes extra data, such as page views and extracted hashtags.
        """
        if collection:
            endpoint = '/api/collections/{}/posts/{}'.format(
                collection, post_id_or_slug)
        else:
            endpoint = '/api/posts/' + post_id_or_slug
        return self._get(endpoint, needs_auth=self.is_authenticated())

    def get_posts(self, collection: str = None) -> List[dict]:
        """Retrieve all posts, or posts from the given collection."""
        if collection:
            endpoint = '/api/collections/{}/posts'.format(collection)
            return self._get(endpoint, needs_auth=True)['posts']
        return self._get('/api/me/posts', needs_auth=True)

    def update_post(self, post_id: str, body: str, **kwargs) -> dict:
        """Update an existing post.

        If done anonymously, it requires past knowledge of the existing
        post's token.
        See https://developers.write.as/docs/api/#update-a-post
        """
        return self._post(
            '/api/posts/' + post_id,
            data={'body': body, **kwargs},
            needs_auth=self.is_authenticated(),
        )

    def delete_post(self, post_id: str, post_token: str = None) -> None:
        """Delete a post.

        If done anonymously, it requires past knowledge of the existing
        post's token.
        """
        self._delete(
            '/api/posts/' + post_id,
            data=post_token and {'token': post_token},
            needs_auth=self.is_authenticated(),
        )

    def claim_post(self, post_id: str, post_token: str) -> dict:
        """Add unowned post to the user/account."""
        return self.claim_posts(
            [{'id': post_id, 'token': post_token}])[0]

    def claim_posts(self, posts: List[dict]) -> List[dict]:
        """Add unowned posts to user/account.

        See https://developers.write.as/docs/api/#claim-posts
        """
        return self._post('/api/posts/claim', data=posts, needs_auth=True)

    def move_post(self, post_id: str, collection: str,
                  post_token: str = None) -> dict:
        """Move a post to a collection.

        Add a post to a collection. This works for either posts that
        were created anonymously (i.e. don't belong to the user account)
        or posts already owned by the user account.
        """
        return self.move_posts(
            [{'id': post_id, 'token': post_token}], collection)[0]

    def move_posts(self, posts: List[dict], collection: str) -> List[dict]:
        """Move posts to a Collection.

        Add a group of posts to a collection. This works for either posts
        that were created anonymously (i.e. don't belong to the user
        account) or posts already owned by the user account.
        See https://developers.write.as/docs/api/#claim-posts
        """
        return self._post(
            '/api/collections/{}/collect'.format(collection),
            data=posts, needs_auth=True)

    def pin_post(self, post_id: str, collection: str,
                 post_position: int = None) -> dict:
        """Pin a post to a collection.

        Pinned posts will show up as a navigation items in the
        collection/blog home page header, instead of on the blog itself.
        """
        return self.pin_posts(
            [{'id': post_id, 'position': post_position}], collection)[0]

    def pin_posts(self, posts: List[dict], collection: str) -> List[dict]:
        """Pin posts to a collection.

        Pinned posts will show up as a navigation items in the
        collection/blog home page header, instead of on the blog itself.
        See https://developers.write.as/docs/api/#pin-a-post-to-a-collection
        """
        return self._post('/api/collections/{}/pin'.format(collection),
                          data=posts, needs_auth=True)

    def unpin_post(self, post_id: str, collection: str) -> dict:
        """Unpin a post from a collection.

        The navigation item will be removed from the collection/blog
        home page header and the post will be back on the blog itself.
        """
        return self.unpin_posts([{'id': post_id}], collection)[0]

    def unpin_posts(self, posts: List[dict], collection: str) -> List[dict]:
        """Unpin posts from a collection.

        The navigation items will be removed from the collection/blog
        home page header and the posts will be back on the blog itself.
        See https://developers.write.as/docs/api/#unpin-a-post-from-a-collection
        """
        return self._post('/api/collections/{}/unpin'.format(collection),
                          data=posts, needs_auth=True)

    # ===== COLLECTIONS =====

    def create_collection(self, alias: str = None, title: str = None) -> dict:
        """Create a new collection.

        Clients must supply either a title or alias (or both). If only
        a title is given, the alias will be generated from it.
        """
        assert alias or title, 'Alias or title should be supplied.'
        return self._post(
            '/api/collections',
            data={'alias': alias, 'title': title},
            needs_auth=True,
        )

    def get_collection(self, alias: str) -> dict:
        """Retrieve a collection and its metadata."""
        return self._get(
            '/api/collections/' + alias,
            needs_auth=self.is_authenticated(),
        )

    def get_collections(self) -> List[dict]:
        """Retrieve user's collections."""
        return self._get('/api/me/collections', needs_auth=True)

    def update_collection(self, alias: str, **kwargs) -> dict:
        """Update attributes of an existing collection.

        Supply only the fields you would like to update. Any fields left
        out will remain unchanged.
        See https://developers.write.as/docs/api/#update-a-collection for
        a list of valid fields.
        """
        return self._post(
            '/api/collections/' + alias, data=kwargs, needs_auth=True)

    def delete_collection(self, alias: str) -> None:
        """Delete a collection.

        Permanently delete a collection and make any posts on it
        anonymous.
        """
        self._delete('/api/collections/' + alias, needs_auth=True)

    def get_channels(self) -> List[dict]:
        """Return a list of the authenticated user's connected channels, or integrations.

        For channels that aren't a centralized service, like Mastodon,
        you'll also see a url property of the specific instance or host
        that the user has connected to.
        """
        return self._get('/api/me/channels')
