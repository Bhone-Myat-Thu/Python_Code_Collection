from email.policy import strict
import requests
import sys
import re
import os


def folderCheck():


    if os.path.exists(f"rawdata\{sys.argv[1].split('.')[0]}"):
        pass
    else:
        os.makedirs(f"rawdata\{sys.argv[1].split('.')[0]}")

    if os.path.exists(f"finalresult\{sys.argv[1].split('.')[0]}"):
        pass
    else:
        os.makedirs(f"finalresult\{sys.argv[1].split('.')[0]}")


    return True


def digicert():




    url = 'https://daas.digicert.com/apicontroller/v1/scan/getSubdomains'

    domain = sys.argv[1]


    header = {
        'X-DC-DEVKEY': 'BTANG4SBCACFOEGYXZWIWGEDLKC2XUZGZAHRVLOHWEDHIM7UEM3S6O4GY62HX7I3UANDQNNIRKBML4CV2',
        'Content-Type': 'application/json'
    } 

    data  = {
        "accountId": "1647476",
        "domains": [f"{domain}"]
        }

    r = requests.post(url,json=data, headers=header)
    # print(r.json())

    # print(json.dumps(r.json(), indent=4))
    for i in r.json()['data'][0]['subdomains']:
        with open(f"rawdata\{sys.argv[1].split('.')[0]}\{sys.argv[1].split('.')[0]}-digicert.txt", "a") as f:
            f.write(i + "\n")

    return f"{sys.argv[1].split('.')[0]}-digicert.txt"




def certspotter():


    

    url = f"https://api.certspotter.com/v1/issuances?domain={sys.argv[1]}&include_subdomains=true&expand=dns_names"

    req = requests.get(url=url)

    for i in range(len(req.json())): # return => list 
        if (req.json()[i]['dns_names']):
            for j in range(len(req.json()[i]['dns_names'])): # extract these list => string

                # print(req.json()[i]['dns_names'][j])


                if re.findall("\*.", req.json()[i]['dns_names'][j]):
                    x = req.json()[i]['dns_names'][j].replace("*.", "")

                    with open(f"rawdata\{sys.argv[1].split('.')[0]}\{sys.argv[1].split('.')[0]}-certspotter.txt", "a") as f:
                        f.write(x  + "\n")

                else:
                    with open(f"rawdata\{sys.argv[1].split('.')[0]}\{sys.argv[1].split('.')[0]}-certspotter.txt", "a") as f:
                        f.write(req.json()[i]['dns_names'][j] + "\n")

    return f"{sys.argv[1].split('.')[0]}-certspotter.txt"



def uniqueness(filename):

    arr = []
    with open(f"..\\..\\finalresult\{sys.argv[1].split('.')[0]}\.{filename}","r") as f:
        s = set(line for line in f)
        for i in list(s):
            arr.append(i)

    with open(f"..\\..\\finalresult\{sys.argv[1].split('.')[0]}\{filename}", "w") as f:
        for i in arr:
            f.write(f"{i}")







def finalresult():

    arr = []


    os.chdir(f"rawdata\{sys.argv[1].split('.')[0]}")
    

    for file in os.listdir():
        if file.endswith("txt"):
            with open(file, "r") as f:

                while True:
                    
                    rea = f.readline()
                    if not rea:
                        break
                    arr.append(rea.strip())

    with open (f"..\\..\\finalresult\{sys.argv[1].split('.')[0]}\.{sys.argv[1].split('.')[0]}-final.txt","w") as fr:

        
        for i in arr:
            fr.write(i +"\n")

    return f"{sys.argv[1].split('.')[0]}-final.txt"







    

    


if __name__ == "__main__":

    print("hellowor ")
    if folderCheck():

        digicert()
        print("ada")

        certspotter()  
        uniqueness(finalresult())



    else:
        print("Somethings Wrong")


    # uniqueness(finalresult())
  
    # print(os.getcwd())




# url -s https://api.certspotter.com/v1/issuances?domain\=$1\&include_subdomains=true\&expand\=dns_names | jq '.[].dns_names[]' | sed 's/\"//g' | sed 's/\*\.//g' | sort -u | grep -w $1\$ | tee rawdata/$1-certspotter.txt
