# -*- coding: utf-8 -*-
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EN_PATH = 'src/json/text.json'
FA_PATH = 'dist/lib/json/lang/fa-IR.json'

with open(EN_PATH, 'r', encoding='utf-8') as f:
    en_dict = json.load(f)

with open(FA_PATH, 'r', encoding='utf-8') as f:
    fa_dict = json.load(f)

print(f"Loaded {len(en_dict)} EN keys, {len(fa_dict)} FA keys.")
