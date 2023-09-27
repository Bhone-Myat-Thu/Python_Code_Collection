import hashlib

hash = "fbbe7e952d1050bfb09dfdb71d4c2ff2b3d845d2"

# print(hashlib.sha1("password".encode()).hexdigest())

def crack_sha1_hash(hash, use_salts=False):
    
        if not use_salts:
            with open("pass.txt") as f:
                while True:
                    line = f.readline().strip()
                    if not line:
                        break
                    else:
                        result = hashlib.sha1(line.encode()).hexdigest()            
                        if hash == result:
                            print(line)
                            break
                        else:
                            print("not")
                            continue
                    
        else:
            with open("pass.txt") as f:
                for line in f:
                    with open("salt.txt") as s:
                        for salt in s:
                            
                            salted_plain = line.strip() + salt.strip()
                            result = hashlib.sha1(salted_plain.encode()).hexdigest()            
                            if hash == result:
                                print(line)
                                break
                                            
crack_sha1_hash(hash, True)