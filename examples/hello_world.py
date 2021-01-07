
import writefreely as wf

# default WriteFreely instance is 'https://write.as'
c = wf.client(user='foo', password='bar')

# saving token to avoid having to login each time:
# with open('my_token.txt', 'w') as fd:
#     fd.write(c.token)
# next time, load token from file:
# with open('my_token.txt') as fd:
#    c = wf.client(token=fd.read())

# post something to "cool-stuff" collection
post = c.create_post(collection='cool-stuff', title='Cool Article', body='Hello world!')
print('Visit your new post at:', post['collection']['url'] + post['slug'])

# c.logout()
# The access token isn't valid anymore if you log out, you have to login
# with user and password again, so don't logout unless you know what you
# are doing
