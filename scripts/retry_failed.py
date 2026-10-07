# -*- coding: utf-8 -*-
import sys
import json
import re
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CACHE_FILE = 'scripts/fa_cache.json'
FA_FILE = 'dist/lib/json/lang/fa-IR.json'
EN_FILE = 'src/json/text.json'

with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    cache = json.load(f)

with open(FA_FILE, 'r', encoding='utf-8') as f:
    fa = json.load(f)

with open(EN_FILE, 'r', encoding='utf-8') as f:
    en = json.load(f)

# Find keys that are still in English
failed_keys = {k: v for k, v in en.items() if fa.get(k) == v and len(v) > 3 and not re.match(r'^[%+\d\s\-.,/\\#@!]+$', v)}
unique_failed = list(set(failed_keys.values()))
print(f"Unique phrases to retry: {len(unique_failed)}")

def translate_safe(text):
    placeholders = re.findall(r'%[sd]|<[^>]+>', text)
    tokenized = text
    for i, p in enumerate(placeholders):
        tokenized = tokenized.replace(p, f' QX{i}QX ', 1)
    
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fa&dt=t&q=' + urllib.parse.quote(tokenized)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode('utf-8'))
                raw = ''.join([part[0] for part in res[0] if part and part[0]])
                restored = raw
                for i, p in enumerate(placeholders):
                    restored = re.sub(rf'QX\s*{i}\s*QX', p, restored, flags=re.IGNORECASE)
                
                restored = restored.replace('Anytype', 'Anytype')
                restored = restored.replace('کانال ها', 'کانال‌ها')
                restored = restored.replace('برگه ها', 'برگه‌ها')
                restored = restored.replace('نوع ها', 'نوع‌ها')
                restored = restored.replace('شیء ها', 'اشیاء')
                restored = restored.replace('ویژگی ها', 'ویژگی‌ها')
                restored = restored.replace('مجموعه ها', 'مجموعه‌ها')
                restored = restored.replace('نشانک ها', 'نشانک‌ها')
                restored = restored.replace('فایل ها', 'فایل‌ها')
                return restored.strip()
        except Exception as e:
            time.sleep(1 + attempt)
    return text

done = 0
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(translate_safe, t): t for t in unique_failed}
    for f in as_completed(futures):
        orig = futures[f]
        res = f.result()
        if res != orig:
            cache[orig] = res
        done += 1
        if done % 20 == 0 or done == len(unique_failed):
            print(f"Retried {done}/{len(unique_failed)}", flush=True)

# Update fa-IR.json with new cache
for k, v in en.items():
    if v in cache:
        fa[k] = cache[v]

with open(FA_FILE, 'w', encoding='utf-8') as f:
    json.dump(fa, f, ensure_ascii=False, indent=4)

with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)

print("Retry completed successfully!", flush=True)
