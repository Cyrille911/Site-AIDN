import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from django.test import Client

c = Client(SERVER_NAME='localhost')
pages = ['/', '/portfolio/', '/a-propos/', '/voir-plus/', '/nous-joindre/']

for p in pages:
    html = c.get(p).content.decode()
    # Find where <nav class="modern-navbar"> is and what comes before it
    idx = html.find('<nav class="modern-navbar">')
    before = html[max(0,idx-300):idx]
    # Find the <body> tag  
    body_idx = html.find('<body')
    body_end = html.find('>', body_idx) + 1
    between = html[body_end:idx].strip()
    print(f"=== {p} ===")
    print(f"Body tag: {html[body_idx:body_end]}")
    print(f"Between <body> and <nav>: [{between[:200]}]")
    
    # Check if nav is inside #wrapper
    wrapper_idx = html.find('id="wrapper"')
    print(f"Nav at index: {idx}, Wrapper at index: {wrapper_idx}")
    if wrapper_idx < idx and wrapper_idx != -1:
        print("  WARNING: Nav might be INSIDE wrapper!")
    else:
        print("  OK: Nav is before wrapper")
    print()
