# screenshot_upload.py
import io
import pyautogui
import requests
from datetime import datetime

def upload_screenshot(server_url):
    """
    Take a screenshot and upload it to server_url (e.g., https://abcd.ngrok.io/upload).
    This function should be called only with explicit user consent (e.g., user clicked a visible button).
    """
    # Take screenshot
    img = pyautogui.screenshot()  # PIL Image

    # Save to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    files = {
        'file': ('screenshot.png', buf, 'image/png')
    }

    try:
        resp = requests.post(server_url, files=files, timeout=10)
        if resp.status_code == 200:
            print("Upload successful")
            return True
        else:
            print("Upload failed:", resp.status_code, resp.text)
            return False
    except Exception as e:
        print("Upload error:", e)
        return False
