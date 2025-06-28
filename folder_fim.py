import time 
import os
import hashlib

folder = "E:\FLUIDECH" #the folder path you want to monitor.
interval = 10

def file_hashv(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as  e:
        print(f"[ERROR] Could not hash {path}: {e}")
        return None 
    
def scan_folder(folder):
    file_hashes = {}
    for root, dirs, files in os.walk(folder):
        for fname in files:
            fpath = os.path.join(root,fname)
            file_hashes[fpath] = file_hashv(fpath)
    return file_hashes
        
def monitor():
    print(f"Monitoring folder: {folder}")
    baseline = scan_folder(folder)

    while True:
        time.sleep(interval)
        current = scan_folder(folder)

        for path in baseline :
            if path not in current:
                print(f"[DELETED] {path}")
            elif baseline[path] != current[path]:
                print(f"[MODIFIED] {path}")

        for path in current:
            if path not in baseline:
                print(f"[NEW FILE] {path}")

        baseline = current 

monitor()


