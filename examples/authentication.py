
import writefreely as wf

c = wf.client(host='qua.name', user='foo', password='bar')

# saving token to avoid login each time:
with open('my_token.txt', 'w') as fd:
    fd.write(c.token)

# create an authenticated post
post = c.create_post(title='Cool Post', body='Awesome content!')
print('See your post at: {}/{}'.format(c.host, post['slug']))

# next time, load token from file:
with open('my_token.txt') as fd:
    c = wf.client(host='qua.name', token=fd.read())

print('User Name:', c.me()['username'])  # User Name: foo

c.logout()
# The access token isn't valid anymore

assert not c.is_authenticated()

# create an anonymous post (not allowed by all instances)
post = c.create_post(title='Anonymous Post', body='Guess who am I?')
print('See your post at: {}/{}'.format(c.host, post['slug']))

c.me()  # raises an error because that request can't be done unauthenticated
