from ast import arg
import ipaddress
import argparse


class Obfuscator:

    def __init__(self, ip :ipaddress.ip_address) -> str:
        self.ip = ipaddress.ip_address(ip)


    def obfuscate(self):
        
        print(f"{'Decimal':<15}: {int(self.ip)}")
        print(f"{'Hexadecimal':<15}: {hex(int(self.ip))}")
        print(f"{'Octal':<15}: {oct(int(self.ip)).replace('o', '0')}")
        
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="ipaddress")

    parser_agrs = parser.parse_args()

    if parser_agrs.ipaddress:
            

        O = Obfuscator(parser_agrs.ipaddress)

        O.obfuscate()

