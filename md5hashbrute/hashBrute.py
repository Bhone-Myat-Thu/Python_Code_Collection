
import sys
import hashlib

hash = sys.argv[1]

# count = 0

with open("passwords.txt") as f:
    
    while True:
        
        # count += 1 
    
        line = f.readline()
        if not line:
            break
        else:
            md5Hash = hashlib.md5(line.strip().encode()).hexdigest() 
            if hash == md5Hash:
                print(f"Your Password is : {line}")
                break