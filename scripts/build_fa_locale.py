# -*- coding: utf-8 -*-
"""
Script to generate complete, high-quality Persian (fa-IR) translations for Anytype.
Preserves all placeholders (%s, %d), HTML tags, whitespace, and capitalization rules.
"""

import json
import re
import os

EN_PATH = 'src/json/text.json'
FA_PATH = 'dist/lib/json/lang/fa-IR.json'

def load_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(p, data):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Dedicated exact translations for specific Anytype keys
EXACT_KEY_MAP = {
    # Layout direction & fonts
    "popupSettingsPersonalLayoutDirection": "چیدمان",
    "popupSettingsPersonalLayoutRtl": "از راست به چپ",
    "popupSettingsPersonalLayoutLtr": "از چپ به راست",
    
    # System types
    "commonTypePage": "برگه",
    "commonTypePages": "برگه‌ها",
    "commonTypeTask": "کار",
    "commonTypeTasks": "کارها",
    "commonTypeCollection": "مجموعه",
    "commonTypeCollections": "مجموعه‌ها",
    "commonTypeBookmark": "نشانک",
    "commonTypeBookmarks": "نشانک‌ها",
    "commonTypeImage": "تصویر",
    "commonTypeImages": "تصاویر",
    "commonTypeNote": "یادداشت",
    "commonTypeNotes": "یادداشت‌ها",
    "commonTypeFile": "فایل",
    "commonTypeFiles": "فایل‌ها",
    "commonTypeVideo": "ویدیو",
    "commonTypeVideos": "ویدیوها",
    "commonTypeAudio": "صدا",
    "commonTypeAudios": "صداها",

    # Header & controls
    "headerShare": "اشتراک‌گذاری",
    "commonShare": "اشتراک‌گذاری",
    "commonSettings": "تنظیمات",
    "editorControlDescription0": "نمایش توضیحات",
    "editorControlDescription1": "پنهان کردن توضیحات",
    "editorControlCover0": "افزودن جلد",
    "editorControlCover1": "تغییر جلد",
    "editorControlIcon0": "افزودن آیکون",
    "editorControlLayout": "تنظیمات",

    # Sidebar sections
    "widgetSection0": "صفحه اصلی و سنجاق‌شده",
    "widgetSection1": "نوع‌ها",
    "widgetSection2": "خوانده‌نشده",
    "widgetSection3": "اخیراً ویرایش‌شده",
    "widgetSection4": "زباله‌دان",
    "widgetSection5": "علاقه‌مندی‌های من",
    "widgetSection6": "درختواره",

    # Sidebar widget types & titles
    "popupSearchTypePages": "برگه‌ها",
    "popupSearchTypeBookmarks": "نشانک‌ها",
    "popupSearchTypeCollections": "مجموعه‌ها",
    "popupSearchTypeTypes": "نوع‌ها",
    "onboardingPrimitivesTypesPages": "برگه‌ها",
    "onboardingPrimitivesTypesBookmarks": "نشانک‌ها",
    "onboardingPrimitivesTypesTasks": "کارها",
    "onboardingPrimitivesTypesCollections": "مجموعه‌ها",
    "widgetRecent": "اخیراً ویرایش‌شده",
    "widgetRecentOpen": "اخیراً بازشده",
    "widgetCollection": "مجموعه‌ها",
    "widgetTreeShowBookmarks": "نمایش نشانک‌ها",

    # Settings titles & labels
    "popupSettingsTitle": "تنظیمات",
    "pageSettingsLanguageTitle": "زبان و منطقه",
    "popupSettingsPersonalSectionLanguage": "زبان",
    "popupSettingsPersonalSpellcheckLanguage": "زبان بررسی املا",
    "popupSettingsPersonalInterfaceLanguage": "زبان رابط کاربری",
    "popupSettingsPersonalSectionDateTime": "تاریخ و زمان",
    "popupSettingsPersonalDateFormat": "قالب تاریخ",
    "popupSettingsPersonalTimeFormat": "قالب زمان",
    "popupSettingsPersonalFirstDayOfWeek": "اولین روز هفته",
    "popupSettingsPersonalSectionAppearance": "ظاهر",
    "popupSettingsPersonalTheme": "پوسته",
    "popupSettingsPersonalThemeDark": "تاریک",
    "popupSettingsPersonalThemeLight": "روشن",
    "popupSettingsPersonalThemeSystem": "سیستم",
    "popupSettingsPersonalFont": "قلم برنامه",
    "popupSettingsPersonalFontSystem": "قلم پیش‌فرض سیستم",
    "popupSettingsPersonalFontDana": "دانا (Dana)",
    "popupSettingsPersonalFontDigikala": "دیجی‌کالا (Digikala)",

    # Days
    "day1": "دوشنبه",
    "day2": "سه‌شنبه",
    "day3": "چهارشنبه",
    "day4": "پنجشنبه",
    "day5": "جمعه",
    "day6": "شنبه",
    "day7": "یکشنبه",
}

print("Loaded base EXACT_KEY_MAP with", len(EXACT_KEY_MAP), "keys")
