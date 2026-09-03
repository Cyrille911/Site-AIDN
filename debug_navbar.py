import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.test import Client
import re

c = Client(SERVER_NAME='localhost')
pages = ['/', '/portfolio/', '/a-propos/', '/voir-plus/', '/nous-joindre/']

for p in pages:
    html = c.get(p).content.decode()
    # Extract the full nav block
    nav_match = re.search(r'<nav class="modern-navbar">(.*?)</nav>', html, re.DOTALL)
    if nav_match:
        nav = nav_match.group(1)
        # Check structure
        has_container = 'navbar-container' in nav
        has_logo = 'navbar-logo' in nav
        has_toggle = 'mobile-menu-toggle' in nav
        has_menu = 'navbar-menu' in nav
        has_right = 'navbar-right' in nav
        has_mob_lang = 'mobile-lang-item' in nav
        menu_items = len(re.findall(r'<li', nav))
        print(f"{p}: container={has_container} logo={has_logo} toggle={has_toggle} menu={has_menu} right={has_right} mobLang={has_mob_lang} items={menu_items}")
    else:
        print(f"{p}: NO NAV FOUND")
    
    # Check if there's a second/duplicate nav or conflicting wrapper
    all_navs = re.findall(r'<nav[^>]*>', html)
    print(f"  Total <nav> tags: {len(all_navs)}: {all_navs}")
    
    # Check for wrapper div that might have overflow:hidden
    wrapper_match = re.search(r'id="wrapper"', html)
    if wrapper_match:
        # Check the structure around it
        idx = html.find('id="wrapper"')
        snippet = html[max(0,idx-50):idx+200]
        print(f"  Wrapper found, nearby: ...{snippet[:100]}...")
    
    # Check the JS at bottom
    js_match = re.search(r'mobileMenuToggle.*?addEventListener', html, re.DOTALL)
    if js_match:
        print(f"  JS toggle: found")
    else:
        print(f"  JS toggle: NOT FOUND")
    print()
