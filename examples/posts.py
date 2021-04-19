import writefreely as wf

c = wf.client(token="XXXXXXX")

# create draft post
draft = c.create_post(title="Cool Post", body="Awesome content!")

# publish draft in collection/blog "my-blog"
post = c.move_post(draft["id"], collection="my-blog")
print("See your post at: {}/my-blog/{}".format(c.host, post["slug"]))

assert c.get_post(draft["id"])["slug"] == post["slug"]

# publish a post directly to a collection
post = c.create_post(
    collection="my-blog", title="Another Post", body="Still **Awesome**"
)
print("See your post at: {}/my-blog/{}".format(c.host, post["slug"]))

# getting a post by slug from a collection
post2 = c.get_post(post["slug"], collection="my-blog")
print("{}: {}".format(post2["title"], post2["body"]))

assert post["id"] == post2["id"]

# getting all posts that are draft (not published to a collection)
drafts = [post for post in c.get_posts() if not post["slug"]]
print(drafts)

# updating a post
updated_post = c.update_post(post["id"], body="new post content", title="New Title")
print("{}: {}".format(updated_post["title"], updated_post["body"]))

# deleting a post
c.delete_post(post2["id"])

# claiming a post
anonymous = wf.client()
anon_post = anonymous.create_post(title="My anonymous post", body="Anonymous body")
c.claim_post(anon_post["id"], anon_post["token"])

# pinning post
c.pin_post(post["id"], collection="my-blog")

# unpinning post
c.unpin_post(post["id"], collection="my-blog")
