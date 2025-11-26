import os
import requests
import time

TARGET_ROOT = r"D:\\"
API_URL = "https://cuddly-acorn-7v947956j56rfxgpg-8000.app.github.dev/learn"

ALLOWED_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.java', '.cpp', '.html', '.css', '.json', '.sql'}

def ingest_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        if len(content) < 50: 
            return

        filename = os.path.basename(filepath)
        print(f"⚡ Transmitting: {filename}...")
        
        payload = {
            "content": f"Filename: {filename}\nPath: {filepath}\n\nContent:\n{content}",
            "category": "college_drive_d"
        }
        
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Synced: {filename}")
        else:
            print(f"❌ Server Reject: {response.text}")

    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")

def scan_drive():
    print(f"🚀 NEXUS Synapse initiated. Scanning Drive D: (COLLEGE)...")
    print(f"📡 Uplink: {API_URL}")
    print("------------------------------------------------")
    
    file_count = 0
    
    for root, dirs, files in os.walk(TARGET_ROOT):
        if '$RECYCLE.BIN' in root or 'System Volume Information' in root:
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                full_path = os.path.join(root, file)
                ingest_file(full_path)
                file_count += 1
                time.sleep(0.1)

    print(f"🏁 Sync Complete. {file_count} documents uploaded.")

if __name__ == "__main__":
    scan_drive()