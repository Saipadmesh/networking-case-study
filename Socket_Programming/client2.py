import socket 
import datetime
SEPARATOR = '<SEPARATOR>'

s = socket.socket()
host = socket.gethostname()
ipAddr = socket.gethostbyname(host)
port = 1234

s.connect((host, port))
lst = [-1, 0, 1, 2, 3, 4, 5]
while True:
    number = int(
        input("0: Add new row\n1: View All\n2: View By Date\n3: View By Priority\n4: View By Source\n5: View By Destination\nEnter option (-1 to break): "))

    if number in lst:
        send_str = str(number)
        if(number == 0):
            x = datetime.datetime.now()
            timestmp = str(x)
            src = input("Enter source: ")
            dest = input("Enter destination: ")
            msg = input("Enter message: ")
            priority = input("Enter priority: ")
            send_str = send_str+SEPARATOR+timestmp+SEPARATOR + \
                src+SEPARATOR+dest+SEPARATOR+msg+SEPARATOR+priority+SEPARATOR+ipAddr
        if(number == 2):
            date = input("Enter Date: ")
            send_str = send_str+SEPARATOR+date
        if(number == 3):
            priority = input("Enter Priority: ")
            send_str = send_str+SEPARATOR+priority
        if(number == 4):
            src = input("Enter Source: ")
            send_str = send_str+SEPARATOR+src
        if(number == 5):
            dest = input("Enter Destination: ")
            send_str = send_str+SEPARATOR+dest
        s.send(bytes(send_str, 'utf-8'))
        if(number == -1):
            break
        print(s.recv(1024).decode())
    else:
        print("Enter a valid number")
    print("\n")
s.close()
