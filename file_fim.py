import hashlib 
import time 
file = "parser1.cpp"
def file_hashv(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
og_hash = file_hashv(file)

while True:
    time.sleep(8)
    new_hash = file_hashv(file)
    if new_hash != og_hash :
        print(f"[ALERT] {file} has been modified! ")
        og_hash = new_hash
