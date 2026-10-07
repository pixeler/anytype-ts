# -*- coding: utf-8 -*-
"""
Generate comprehensive Persian translations for Anytype.
"""
import json
import re

EN_PATH = 'src/json/text.json'
FA_PATH = 'dist/lib/json/lang/fa-IR.json'

with open(EN_PATH, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

with open(FA_PATH, 'r', encoding='utf-8') as f:
    fa_data = json.load(f)

print(f"Original: {len(en_data)} en keys, {len(fa_data)} fa keys")
