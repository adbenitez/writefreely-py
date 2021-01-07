
import writefreely as wf

c = wf.client(token='XXXXXXX')

for blog in c.get_collections():
    print('{}: {}'.format(blog['title'], blog['description']))
