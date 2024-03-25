import pikepdf
import sys

def brute_force():
    pdf = sys.argv[1]

    # load password list
    passwords = [ line.strip() for line in open("wordlist.txt") ]

    print("Start Brute Forcing!")

    # iterate over passwords
    for password in passwords:
        try:
            # open PDF file
            with pikepdf.open(pdf, password=password) as pdf:
                # Password decrypted successfully, break out of the loop
                print("[+] Password found:", password)
                break
        except pikepdf._core.PasswordError as e:
            # wrong password, just continue in the loop
            continue
        
def main():

    if len(sys.argv) != 2:
        print("(+) Usage: pdfpassbrute.py document.pdf")
        sys.exit(-1)
    else:
        brute_force()
        
if __name__ == "__main__":
    main()