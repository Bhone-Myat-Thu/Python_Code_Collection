import shodan
from colorama import Fore
import argparse


def test_key(key):

    """
        checking whether the key is valid or not:
        if valid and paid version   => true, true
        if valid and not paid       => true, false
        if not valid and not paid   => false, false
    
    """


    api = shodan.Shodan(key)

    try:    
        information = api.info()
    except Exception:
        return False, False

    if information["plan"] == "dev" or information["plan"] == "edu":
        return True,True

    elif information["plan"] == "oss":
        return True,False


def test_list(keyList):

    """
        checking for the list

    """

    try:
        f = open(keyList)
        
        keys = f.readlines()
        for key in keys:
            key=key.strip()
            valid, paid = test_key(key=key)

            checking(valid=valid,paid=paid,key=key) #calling function

    except Exception as err:
        print(err)


def checking(valid,paid,key):

    """

        for printing the result

    """

    if valid == True and paid == True:
        print(f"The Key '{key}' is" + Fore.GREEN + " valid" +Fore.WHITE +" and " + Fore.GREEN + "Paid" + Fore.WHITE)

    elif valid == True and paid == False:
        print(f"The Key '{key}' is" + Fore.GREEN + " valid" + Fore.WHITE + " but " + Fore.RED + "Not Paid" + Fore.WHITE)

    elif valid == False and paid == False:
        print(f"The Key '{key}' is" + Fore.RED + " Not Valid" +Fore.WHITE +" and " + Fore.RED + "Not Paid" + Fore.WHITE)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', dest="list", help="-l [listFile.txt]")
    parser.add_argument('-k', dest="key", help="-k KEY")


    parser_args = parser.parse_args()


    if parser_args.list:
        test_list(parser_args.list)
 
    elif parser_args.key:
        valid, paid = test_key(parser_args.key)
    
        checking(valid=valid,paid=paid,key=parser_args.key)
    
