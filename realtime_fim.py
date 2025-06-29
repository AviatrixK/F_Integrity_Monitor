import os 
import time 
import hashlib 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_hashes = {}
important_ext = ('.conf','.docx','.exe') #only  files having these extensions will be monitored.

def get_file_hash(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"[ERROR] could not hash {path}: {e}")
        return None
    
class FIMHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(important_ext):
            return
        
        new_hash = get_file_hash(event.src_path)
        if new_hash is None:
            return 

        old_hash = file_hashes.get(event.src_path)
        if old_hash != new_hash:
            print(f"[MODIFIED] {event.src_path}") 
            file_hashes[event.src_path] = new_hash

    def on_created(self, event):
        if event.is_directory:
            return
        
        if not event.src_path.endswith(important_ext):
            return
        
        file_hash = get_file_hash(event.src_path)
        if file_hash:
            file_hashes[event.src_path] = file_hash
            print(f"[CREATED] {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        if event.src_path in file_hashes:
            print(f"[DELETED] {event.src_path}")
            file_hashes.pop(event.src_path,None)

    def on_moved(self,event):
        if event.is_directory:
            return
        if event.src_path in file_hashes:
            print(f"[MOVED] {event.src_path} -> {event.dest_path}")
            file_hashes[event.dest_path] = file_hashes.pop(event.src_path)

def initialize_hashes(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root,file)
            if full_path.endswith(important_ext):
                hash_val = get_file_hash(full_path)
                if hash_val:
                    file_hashes[full_path] = hash_val

if __name__ == "__main__":
    watch_path = r"E:/FLUIDECH"
    initialize_hashes(watch_path)
    event_handler = FIMHandler()
    observer = Observer()
    observer.schedule(event_handler, path = watch_path, recursive=True)
    observer.start()
    print(f"Folder Integrity Monitor Started: {watch_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
