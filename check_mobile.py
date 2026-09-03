import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.test import Client

c = Client(SERVER_NAME='localhost')
pages = ['/', '/portfolio/', '/a-propos/', '/voir-plus/', '/nous-joindre/']

for p in pages:
    html = c.get(p).content.decode()
    toggle = 'id="mobile-menu-toggle"' in html
    menu = 'id="navbar-menu"' in html
    js = 'mobileMenuToggle' in html
    mob_lang = 'mobile-lang-item' in html
    print(f"{p}: toggle={toggle} menu={menu} js={js} mobLang={mob_lang}")
