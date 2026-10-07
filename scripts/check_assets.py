import os, re

base = r'dist\win-unpacked\resources\app.asar.unpacked\dist'
html_path = os.path.join(base, 'index.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

srcs = re.findall(r'(?:src|href)="([^"]+)"', html)
print('Checking references in win-unpacked index.html:')
all_ok = True
for s in srcs:
    s_clean = s.lstrip('./').replace('/', os.sep)
    target = os.path.join(base, s_clean)
    exists = os.path.exists(target)
    print(f'  {s} -> exists: {exists}')
    if not exists:
        all_ok = False

print('All assets exist:', all_ok)
