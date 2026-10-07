# -*- coding: utf-8 -*-
import sys, re, urllib.request, urllib.parse, json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

text = 'Move %s "%s" to Bin?'
placeholders = re.findall(r'%[sd]|<[^>]+>', text)
tokenized = text
for i, p in enumerate(placeholders):
    tokenized = tokenized.replace(p, f'XYZ{i}XYZ', 1)

print('Tokenized:', tokenized)
url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fa&dt=t&q=' + urllib.parse.quote(tokenized)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=5) as response:
    res = json.loads(response.read().decode('utf-8'))
    translated = res[0][0][0]

print('Raw translated:', translated)
for i, p in enumerate(placeholders):
    translated = re.sub(rf'XYZ\s*{i}\s*XYZ', p, translated, flags=re.IGNORECASE)

print('Restored:', translated)
