# -*- coding: utf-8 -*-
"""
Comprehensive Persian (fa-IR) translation builder for Anytype.
"""
import json
import re

EN_PATH = 'src/json/text.json'
FA_PATH = 'dist/lib/json/lang/fa-IR.json'

with open(EN_PATH, 'r', encoding='utf-8') as f:
    en_dict = json.load(f)

with open(FA_PATH, 'r', encoding='utf-8') as f:
    fa_dict = json.load(f)

# 1. Exact key overrides
EXACT_KEY = {
    # Layout and Direction
    "popupSettingsPersonalLayoutDirection": "چیدمان",
    "popupSettingsPersonalLayoutRtl": "از راست به چپ",
    "popupSettingsPersonalLayoutLtr": "از چپ به راست",

    # System Types
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

    # Header and Controls
    "commonShare": "اشتراک‌گذاری",
    "headerShare": "اشتراک‌گذاری",
    "commonSettings": "تنظیمات",
    "commonDescription": "توضیحات",
    "editorControlDescription0": "نمایش توضیحات",
    "editorControlDescription1": "پنهان کردن توضیحات",
    "editorControlCover0": "افزودن جلد",
    "editorControlCover1": "تغییر جلد",
    "editorControlIcon0": "افزودن آیکون",
    "editorControlLayout": "تنظیمات",

    # Sidebar Sections
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
    "popupSearchTypeTasks": "کارها",
    "onboardingPrimitivesTypesPages": "برگه‌ها",
    "onboardingPrimitivesTypesBookmarks": "نشانک‌ها",
    "onboardingPrimitivesTypesTasks": "کارها",
    "onboardingPrimitivesTypesCollections": "مجموعه‌ها",
    "widgetRecent": "اخیراً ویرایش‌شده",
    "widgetRecentOpen": "اخیراً بازشده",
    "widgetCollection": "مجموعه‌ها",
    "widgetTreeShowBookmarks": "نمایش نشانک‌ها",
    "popupSearchRecentEdited": "اخیراً ویرایش‌شده",
    "popupSearchRecentCreated": "اخیراً ایجاد‌شده",
    "popupSearchRecentUsed": "اخیراً استفاده‌شده",
    "popupSearchRecentActive": "اخیراً فعال",

    # Settings titles & sections
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

print(f"Loaded {len(EXACT_KEY)} exact keys")
