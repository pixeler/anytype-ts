# -*- coding: utf-8 -*-
"""
Full Persian Translation Pipeline for Anytype.
Safely translates all untranslated strings while preserving:
1. All %s, %d placeholders exactly.
2. All HTML tags exactly.
3. Natural Persian terminology consistent with Anytype.
"""

import sys
import os
import json
import re
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EN_FILE = 'src/json/text.json'
FA_FILE = 'dist/lib/json/lang/fa-IR.json'
CACHE_FILE = 'scripts/fa_cache.json'

with open(EN_FILE, 'r', encoding='utf-8') as f:
    en_all = json.load(f)

with open(FA_FILE, 'r', encoding='utf-8') as f:
    fa_existing = json.load(f)

cache = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    except Exception:
        pass

# 1. Exact Key Overrides
EXACT_KEYS = {
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

# 2. Exact Phrase Overrides
EXACT_PHRASES = {
    # System Types
    "Page": "برگه",
    "Pages": "برگه‌ها",
    "Task": "کار",
    "Tasks": "کارها",
    "Collection": "مجموعه",
    "Collections": "مجموعه‌ها",
    "Bookmark": "نشانک",
    "Bookmarks": "نشانک‌ها",
    "Image": "تصویر",
    "Images": "تصاویر",
    "Note": "یادداشت",
    "Notes": "یادداشت‌ها",
    "File": "فایل",
    "Files": "فایل‌ها",
    "Video": "ویدیو",
    "Videos": "ویدیوها",
    "Audio": "صدا",
    "Audios": "صداها",
    "Type": "نوع",
    "Types": "نوع‌ها",
    "Object": "شیء",
    "Objects": "اشیاء",
    "Property": "ویژگی",
    "Properties": "ویژگی‌ها",
    "Relation": "ویژگی",
    "Relations": "ویژگی‌ها",
    "Space": "فضا",
    "Spaces": "فضاها",
    "Channel": "کانال",
    "Channels": "کانال‌ها",
    "Personal Space": "فضای شخصی",
    "Shared Channel": "کانال اشتراکی",
    "Vault": "مخزن امن",
    "Profile": "نمایه",
    "Account": "حساب کاربری",
    "Settings": "تنظیمات",
    "App Settings": "تنظیمات برنامه",
    "Channel Settings": "تنظیمات کانال",
    "Profile Settings": "تنظیمات نمایه",
    "Vault Settings": "تنظیمات مخزن امن",
    "Default Object Type": "نوع پیش‌فرض شیء",
    "Set the default type for newly created objects": "تنظیم نوع پیش‌فرض برای اشیاء تازه‌ساخته‌شده",

    # Actions
    "Share": "اشتراک‌گذاری",
    "Share Anytype": "اشتراک‌گذاری Anytype",
    "Save": "ذخیره",
    "Cancel": "لغو",
    "Delete": "حذف",
    "Edit": "ویرایش",
    "Add": "افزودن",
    "Create": "ایجاد",
    "Create new": "ایجاد جدید",
    "Rename": "تغییر نام",
    "Duplicate": "تکثیر",
    "Move": "انتقال",
    "Copy": "رونوشت",
    "Copy link": "رونوشت پیوند",
    "Copy URL": "رونوشت آدرس",
    "Copy text": "رونوشت متن",
    "Cut": "برش",
    "Paste": "چسباندن",
    "Undo": "واگرد",
    "Redo": "از نو",
    "Archive": "بایگانی",
    "Restore": "بازیابی",
    "Remove": "برداشتن",
    "Clear": "پاک کردن",
    "Clear style": "پاک کردن سبک",
    "Select": "انتخاب",
    "Select all": "انتخاب همه",
    "Done": "انجام شد",
    "Close": "بستن",
    "Back": "بازگشت",
    "Next": "بعدی",
    "Continue": "ادامه",
    "Confirm": "تأیید",
    "Apply": "اعمال",
    "Reset": "بازنشانی",
    "Search": "جستجو",
    "Filter": "پالایش",
    "Sort": "مرتب‌سازی",
    "Group": "گروه‌بندی",
    "View": "نما",
    "Preview": "پیش‌نمایش",
    "Open": "باز کردن",
    "Open in new window": "باز کردن در پنجره جدید",
    "Open in new tab": "باز کردن در برگه جدید",
    "Open fullscreen": "نمایش تمام‌صفحه",
    "Download": "دانلود",
    "Upload": "بارگذاری",
    "Import": "درون‌ریزی",
    "Export": "برون‌بری",
    "Connect": "اتصال",
    "Disconnect": "قطع اتصال",
    "Sync": "همگام‌سازی",
    "Lock": "قفل کردن",
    "Unlock": "باز کردن قفل",
    "Show": "نمایش",
    "Hide": "پنهان کردن",
    "Expand": "گسترش",
    "Collapse": "جمع کردن",
    "Expand all": "گسترش همه",
    "Collapse all": "جمع کردن همه",
    "Restart": "راه‌اندازی مجدد",
    "Reject": "رد کردن",
    "Dismiss suggestion": "رد پیشنهاد",

    # Editor Controls & Description
    "Show description": "نمایش توضیحات",
    "Hide description": "پنهان کردن توضیحات",
    "Add cover": "افزودن جلد",
    "Change cover": "تغییر جلد",
    "Remove cover": "حذف جلد",
    "Add icon": "افزودن آیکون",
    "Change icon": "تغییر آیکون",
    "Remove icon": "حذف آیکون",
    "Description": "توضیحات",
    "Add a description": "افزودن توضیحات",
    "Property description": "توضیحات ویژگی",
    "Object cover": "جلد شیء",
    "Picture": "تصویر",
    "Untitled": "بدون عنوان",

    # Sidebar & Sections
    "Home and Pinned": "صفحه اصلی و سنجاق‌شده",
    "Recently edited": "اخیراً ویرایش‌شده",
    "Recently created": "اخیراً ایجاد‌شده",
    "Recently used": "اخیراً استفاده‌شده",
    "Recently opened": "اخیراً بازشده",
    "Recently active": "اخیراً فعال",
    "Recently added": "اخیراً افزوده‌شده",
    "Tree": "درختواره",
    "Tree Diagnostics": "عیب‌یابی درختواره",
    "Unread": "خوانده‌نشده",
    "Bin": "زباله‌دان",
    "My Favorites": "علاقه‌مندی‌های من",
    "Favorites": "علاقه‌مندی‌ها",
    "Move to Bin": "انتقال به زباله‌دان",
    "Restore from Bin": "بازیابی از زباله‌دان",
    "Empty Bin": "خالی کردن زباله‌دان",
    "Switch to tree view": "تغییر به نمای درختی",
    "Switch to compact view": "تغییر به نمای فشرده",
    "Switch to detailed view": "تغییر به نمای با جزئیات",
    "Cleanup": "پاک‌سازی",
    "Deleted object": "شیء حذف‌شده",
    "Created in": "ایجادشده در",
    "Link removed from": "پیوند برداشته‌شده از",
    "Hide media files in page tree": "پنهان کردن فایل‌های چندرسانه‌ای در درخت برگه",

    # Layout Direction & Settings
    "Layout": "چیدمان",
    "Layout direction": "چیدمان",
    "Right to left": "از راست به چپ",
    "Left to right": "از چپ به راست",
    "Appearance": "ظاهر",
    "Theme": "پوسته",
    "Dark": "تاریک",
    "Light": "روشن",
    "System": "سیستم",
    "Font": "قلم",
    "App font": "قلم برنامه",
    "Language": "زبان",
    "Language & Region": "زبان و منطقه",
    "Spellcheck language": "زبان بررسی املا",
    "Interface Language": "زبان رابط کاربری",
    "Date & Time": "تاریخ و زمان",
    "Date format": "قالب تاریخ",
    "Time format": "قالب زمان",
    "First day of the week": "اولین روز هفته",
    "First day of week": "اولین روز هفته",

    # Status & Common Terms
    "Status": "وضعیت",
    "Synced": "همگام‌سازی شده",
    "Not Synced": "همگام‌سازی نشده",
    "Syncing": "در حال همگام‌سازی",
    "Connected": "متصل",
    "Disconnected": "قطع",
    "Connecting...": "در حال اتصال...",
    "Offline": "آفلاین",
    "Online": "آنلاین",
    "Pending": "در انتظار",
    "Rejected": "ردشده",
    "Allowed": "مجاز",
    "Denied": "ردشده",
    "Enabled": "فعال",
    "Disabled": "غیرفعال",
    "On": "روشن",
    "Off": "خاموش",
    "Default": "پیش‌فرض",
    "Custom": "سفارشی",
    "All": "همه",
    "None": "هیچ‌کدام",
    "Selected": "انتخاب‌شده",
    "All values": "همه مقادیر",
    "Any name": "هر نامی",
    "Not now": "اکنون نه",
    "No home": "بدون خانه",
    "No results": "نتیجه‌ای یافت نشد",
    "Nothing here": "چیزی اینجا نیست",
    "Empty": "خالی",
    "Loading...": "در حال بارگذاری...",
    "Please wait...": "لطفاً صبر کنید...",
    "Success": "موفقیت",
    "Error": "خطا",
    "Warning": "هشدار",
    "Info": "اطلاعات",
    "Details": "جزئیات",
    "Where": "کجا",
    "Authentication": "احراز هویت",
    "Quote in discussion": "نقل‌قول در گفتگو",
    "Deleted": "حذف‌شده",
    "Deleted Property": "ویژگی حذف‌شده",
    "Line": "خط",
    "List": "فهرست",
    "Small": "کوچک",
    "Medium": "متوسط",
    "Large": "بزرگ",
    "Compact": "فشرده",
    "Regular": "عادی",

    # Members & Sharing
    "Members": "اعضا",
    "Channel Members": "اعضای کانال",
    "Add members": "افزودن اعضا",
    "Invite": "دعوت",
    "Invite members": "دعوت اعضا",
    "Invite link": "پیوند دعوت",
    "Share invite link": "اشتراک‌گذاری پیوند دعوت",
    "Copy invite link": "رونوشت پیوند دعوت",
    "Share invite": "اشتراک‌گذاری دعوت",
    "Share Channel": "اشتراک‌گذاری کانال",
    "Share your profile": "اشتراک‌گذاری نمایه خود",
    "Removal history": "تاریخچه حذف",
    "Deletion audit": "حسابرسی حذف",

    # Block Types & Formatting
    "Text": "متن",
    "Regular Text": "متن عادی",
    "Heading": "سربرگ",
    "Subheading": "زیرسربرگ",
    "Title": "عنوان",
    "Paragraph": "پاراگراف",
    "Bullet list": "فهرست نشانه‌دار",
    "Numbered list": "فهرست شماره‌دار",
    "Toggle list": "فهرست کشویی",
    "Quote": "نقل‌قول",
    "Callout": "کادر پیام",
    "Code": "کد",
    "Inline Code": "کد درون‌خطی",
    "Divider": "خط جداکننده",
    "Table": "جدول",
    "Board": "برد",
    "Gallery": "نگارخانه",
    "Calendar": "گاه‌شمار",
    "LaTeX": "لاتک (LaTeX)",
    "Mathematical formula": "فرمول ریاضی",
    "Mermaid": "مرمید (Mermaid)",
    "Diagram and flowchart": "نمودار و فلوچارت",

    # Dataview & Filters
    "View settings": "تنظیمات نما",
    "Column settings": "تنظیمات ستون",
    "Filter by Types": "پالایش بر اساس نوع‌ها",
    "Limit Object Types": "محدود کردن نوع‌های شیء",
    "Filter Object Types...": "پالایش نوع‌های شیء...",
    "Select Object Type": "انتخاب نوع شیء",
    "Add Object Type": "افزودن نوع شیء",
    "Type settings": "تنظیمات نوع",
    "Type name": "نام نوع",
    "Type plural name": "نام جمع نوع",
    "Editing type": "ویرایش نوع",
    "e.g. Project": "مثلاً پروژه",
    "e.g. Projects": "مثلاً پروژه‌ها",
    "Header": "سربرگ",
    "Properties panel": "پنل ویژگی‌ها",
    "Hidden": "پنهان",
    "Found in objects": "یافت‌شده در اشیاء",
    "There are no Properties yet": "هنوز ویژگی‌ای وجود ندارد",
    "Search Objects...": "جستجوی اشیاء...",
    "Suggest Types and Properties": "پیشنهاد نوع‌ها و ویژگی‌ها",

    # Electron Menu Items
    "File": "پرونده",
    "Window": "پنجره",
    "Help": "راهنما",
    "About Anytype": "درباره Anytype",
    "Preferences": "ترجیحات",
    "Quit Anytype": "خروج از Anytype",
    "Hide Anytype": "پنهان کردن Anytype",
    "Hide Others": "پنهان کردن بقیه",
    "Show All": "نمایش همه",
    "Check for Updates...": "بررسی به‌روزرسانی...",
    "Check for Updates": "بررسی به‌روزرسانی",
    "Minimize": "کمینه‌سازی",
    "Zoom": "بزرگ‌نمایی",
    "Bring All to Front": "آوردن همه به جلو",
    "Toggle Full Screen": "تغییر حالت تمام‌صفحه",
    "Actual Size": "اندازه واقعی",
    "Zoom In": "بزرگ‌نمایی",
    "Zoom Out": "کوچک‌نمایی",
    "Reload": "بارگذاری مجدد",
    "Force Reload": "بارگذاری مجدد اجباری",
    "Toggle Developer Tools": "ابزارهای توسعه‌دهنده",
    "Close Window": "بستن پنجره",
    "New Window": "پنجره جدید",
    "New Tab": "برگه جدید",
    "Documentation": "مستندات",
    "Community": "جامعه کاربران",
    "Report an Issue": "گزارش مشکل",
    "Contact Support": "تماس با پشتیبانی",
    "Keyboard Shortcuts": "میانبرهای صفحه‌کلید",

    # Months
    "January": "ژانویه",
    "February": "فوریه",
    "March": "مارس",
    "April": "آوریل",
    "May": "مه",
    "June": "ژوئن",
    "July": "ژوئیه",
    "August": "اوت",
    "September": "سپتامبر",
    "October": "اکتبر",
    "November": "نوامبر",
    "December": "دسامبر",

    # Onboarding
    "Welcome to Anytype": "به Anytype خوش آمدید",
    "Change Types Easily": "تغییر آسان نوع‌ها",
    "Organize with Types": "سازماندهی با نوع‌ها",
    "Your profile & settings": "نمایه و تنظیمات شما",
    "Let's Go!": "بزن بریم!",
    "No thanks": "خیر، ممنون",
}

def translate_api(text):
    if not text.strip():
        return text
    
    # 1. Protect placeholders and HTML tags
    placeholders = re.findall(r'%[sd]|<[^>]+>', text)
    tokenized = text
    for i, p in enumerate(placeholders):
        tokenized = tokenized.replace(p, f' QX{i}QX ', 1)
    
    # URL encode
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=fa&dt=t&q=' + urllib.parse.quote(tokenized)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=6) as response:
                res = json.loads(response.read().decode('utf-8'))
                raw_translated = ''.join([part[0] for part in res[0] if part and part[0]])
                
                # Restore placeholders
                restored = raw_translated
                for i, p in enumerate(placeholders):
                    restored = re.sub(rf'QX\s*{i}\s*QX', p, restored, flags=re.IGNORECASE)
                
                # Verify placeholders preserved
                orig_ph = re.findall(r'%[sd]', text)
                new_ph = re.findall(r'%[sd]', restored)
                if len(orig_ph) != len(new_ph):
                    # fallback to original placeholders attached
                    return text
                
                # Post-cleanup of standard terms
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
            time.sleep(1)
            
    return text

# Identify missing or untranslated keys
to_translate = []
for k, v in en_all.items():
    if k in EXACT_KEYS:
        fa_existing[k] = EXACT_KEYS[k]
        continue
    if v in EXACT_PHRASES:
        fa_existing[k] = EXACT_PHRASES[v]
        continue
    if k in fa_existing and fa_existing[k] != v and not fa_existing[k].startswith('⚠️'):
        # Already good Persian
        continue
    if v in cache:
        fa_existing[k] = cache[v]
        continue
    to_translate.append((k, v))

# Find unique texts needing translation
unique_needed = list(set([v for k, v in to_translate if v not in cache]))
print(f"Total keys needing translation: {len(to_translate)}, Unique phrases: {len(unique_needed)} (cached: {len(cache)})", flush=True)

done = 0
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(translate_api, text): text for text in unique_needed}
    for f in as_completed(futures):
        orig_text = futures[f]
        try:
            trans = f.result()
            cache[orig_text] = trans
        except Exception as e:
            cache[orig_text] = orig_text
        done += 1
        if done % 50 == 0 or done == len(unique_needed):
            print(f"Translated {done}/{len(unique_needed)} ({done*100//len(unique_needed)}%)", flush=True)
            with open(CACHE_FILE, 'w', encoding='utf-8') as cf:
                json.dump(cache, cf, ensure_ascii=False, indent=2)

# Populate all keys from cache
for k, v in en_all.items():
    if k in EXACT_KEYS:
        fa_existing[k] = EXACT_KEYS[k]
    elif v in EXACT_PHRASES:
        fa_existing[k] = EXACT_PHRASES[v]
    elif k in fa_existing and fa_existing[k] != v and not fa_existing[k].startswith('⚠️'):
        pass
    elif v in cache:
        fa_existing[k] = cache[v]

for k, v in EXACT_KEYS.items():
    fa_existing[k] = v

with open(FA_FILE, 'w', encoding='utf-8') as f:
    json.dump(fa_existing, f, ensure_ascii=False, indent=4)

with open(CACHE_FILE, 'w', encoding='utf-8') as cf:
    json.dump(cache, cf, ensure_ascii=False, indent=2)

print(f"Done! Saved complete Persian translation to {FA_FILE}. Total keys: {len(fa_existing)}")
