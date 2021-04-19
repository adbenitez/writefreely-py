import writefreely as wf

# default WriteFreely instance is 'https://write.as'
c = wf.client(user="foo", password="bar")

# create a post
post = c.create_post(title="Hello World!", body="Hello from **Python**")

print("See your post at: {}/{}".format(c.host, post["slug"]))

# discard current session, invalidate authentication token
c.logout()
