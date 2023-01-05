from pyfirmata import Arduino, util
from datetime import datetime
import smtplib
import time
import json


"""
currently written for three lead readings
add analog pins and digital pins for more leads
"""
def init():
    with open('credentials.json', 'r') as file: #read in json
        credential = json.load(file)
    sender = credential["sender"]
    receiver = credential["receiver"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, credential["password"])
    board = Arduino('/dev/ttyACM0')
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    board.analog[1].enable_reporting()
    board.analog[2].enable_reporting()
    board.analog[3].enable_reporting()
    board.analog[4].enable_reporting()
    board.analog[5].enable_reporting()
    board.digital[5].write(1)
    board.digital[6].write(1)
    board.digital[7].write(1)
    time.sleep(3)
    print("running")
    read(board,server,sender,receiver)


"""
main reading function

checking for any abnormalities, faster than applying entire diagnosis in this main driver function
if abnormalities are detected, moves to broke function for further diagnosis
"""
def read(board,server,sender,receiver):
    while True:
        read1 = board.analog[0].read()
        read2 = board.analog[1].read()
        read3 = board.analog[2].read()
        read4 = board.analog[3].read()
        read5 = board.analog[4].read()
        read6 = board.analog[5].read()
        if read1 < 0.2 or read2 < 0.2:
            broke1(board,read1,read2,read3,read4,read5,read6,server,sender,receiver)
            break
        elif read3 < 0.2 or read4 < 0.2:
            broke2(board,read1,read2,read3,read4,read5,read6,server,sender,receiver)
            break
        elif read5 < 0.2 or read6 < 0.2:
            broke3(board,read1,read2,read3,read4,read5,read6,server,sender,receiver)
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "\n")

"""
all broke functions analyze break of which specific wire
for loop is used to ensure power has flowed through resistors
"""
def broke1(board,read1,read2,read3,read4,read5,read6,server,sender,receiver):
    break1 = False
    breal2 = False
    break3 = False
    for i in range(100000):
        read1 = board.analog[0].read()
        read2 = board.analog[1].read()
        if read1 < 0.2 and read2 < 0.2:
            break1 = True
            break2 = False
            break3 = False
            break
        if read1 < 0.2 and read2 > 0.2:
            break2 = True
            break3 = False
        if read1 > 0.2 and read2 < 0.2:
            break2 = False
            break3 = True
    if break1:
        print("lead 1 broken 1")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 1\nWire 1")
    if break2:
        print("lead 1 broken 2")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 1\nWire 2")
    if break3:
        print("lead 1 broken 3")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 1\nWire 3")
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "\n")

def broke2(board,read1,read2,read3,read4,read5,read6,server,sender,receiver):
    break1 = False
    breal2 = False
    break3 = False
    for i in range(100000):
        read3 = board.analog[2].read()
        read4 = board.analog[3].read()
        if read3 < 0.2 and read4 < 0.2:
            break1 = True
            break2 = False
            break3 = False
            break
        if read3 < 0.2 and read4 > 0.2:
            break2 = True
            break3 = False
        if read3 > 0.2 and read4 < 0.2:
            break2 = False
            break3 = True
    if break1:
        print("lead 2 broken 1")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 2\nWire 1")
    if break2:
        print("lead 2 broken 2")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 2\nWire 2")
    if break3:
        print("lead 2 broken 3")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 2\nWire 3")
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "\n")

def broke3(board,read1,read2,read3,read4,read5,read6,server,sender,receiver):
    break1 = False
    breal2 = False
    break3 = False
    for i in range(100000):
        read5 = board.analog[4].read()
        read6 = board.analog[5].read()
        if read5 < 0.2 and read6 < 0.2:
            break1 = True
            break2 = False
            break3 = False
            break
        if read5 < 0.2 and read6 > 0.2:
            break2 = True
            break3 = False
        if read5 > 0.2 and read6 < 0.2:
            break2 = False
            break3 = True
    if break1:
        print("lead 3 broken 1")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 3\nWire 1")
    if break2:
        print("lead 3 broken 2")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 3\nWire 2")
    if break3:
        print("lead 3 broken 3")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 3\nWire 3")
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "\n")


if __name__ == '__main__':
    init()
