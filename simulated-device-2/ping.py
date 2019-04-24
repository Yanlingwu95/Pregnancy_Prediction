import os

def check_ping():
    hostname = "192.168.56.1" #"10.132.2.174" #"172.217.12.142"
    response = os.system("ping " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus

pingstatus = check_ping()
print(pingstatus)