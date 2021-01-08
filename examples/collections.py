
import writefreely as wf

c = wf.client(token='XXXXXXX')

# creating a collection
c.create_collection(alias='my-blog', title='My Blog')

# getting one collection
blog = c.get_collection('my-blog')
print('Title: {}\nDescription: {}\nURL:{}'.format(
    blog['title'], blog['description'], blog['url']))

# getting all collections
for b in c.get_collections():
    print('{} has {} views and {} posts.'.format(
        b['title'], b['views'], b['total_posts']))

# updating a collection
c.update_collection(
    'my-blog',
    title='New title',
    visibility=1,  # make blog public
)

# deleting a collection
c.delete_collection('my-blog')
