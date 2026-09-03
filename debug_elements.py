import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.test import Client

c = Client(SERVER_NAME='localhost')
pages = ['/', '/portfolio/', '/a-propos/', '/voir-plus/', '/nous-joindre/']

for p in pages:
    html = c.get(p).content.decode()
    elems = {
        '#wrapper': 'id="wrapper"' in html,
        '#header': 'id="header"' in html,
        '#nav': 'id="nav"' in html,
        '#main': 'id="main"' in html,
        '#intro': 'id="intro"' in html,
    }
    print(f"{p}: {elems}")
