# -*- coding: utf-8 -*-
"""
Build all Persian translations for Anytype.
"""
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/untranslated.json', 'r', encoding='utf-8') as f:
    untranslated = json.load(f)

print(f"Total keys to translate: {len(untranslated)}")
