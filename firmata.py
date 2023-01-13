from pyfirmata import Arduino, util, INPUT
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
    board.digital[2].mode = INPUT
    board.digital[3].mode = INPUT
    board.digital[4].mode = INPUT
    board.digital[5].mode = INPUT
    board.digital[6].mode = INPUT
    board.digital[7].mode = INPUT
    board.digital[8].mode = INPUT
    board.digital[9].mode = INPUT
    board.digital[10].mode = INPUT
    board.digital[11].mode = INPUT
    board.digital[12].mode = INPUT
    board.digital[13].mode = INPUT
    it = util.Iterator(board)
    it.start()
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
        read1 = board.digital[2].read()
        read2 = board.digital[3].read()
        read3 = board.digital[4].read()
        read4 = board.digital[5].read()
        read5 = board.digital[6].read()
        read6 = board.digital[7].read()
        read7 = board.digital[8].read()
        read8 = board.digital[9].read()
        read9 = board.digital[10].read()
        read10 = board.digital[11].read()
        read11 = board.digital[12].read()
        read12 = board.digital[13].read()
        if not read1 or not read2: #if any values are false (values are normally true)
            broke(board,2,3,1,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver)
            break
        elif not read3 or not read4:
            broke(board,4,5,2,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver)
            break
        elif not read5 or not read6:
            broke(board,6,7,3,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver)
            break
        elif not read7 or not read8: #if any values are false (values are normally true)
            broke(board,8,9,4,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver)
            break
        elif not read9 or not read10:
            broke(board,10,11,5,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver)
            break
        elif not read11 or not read12:
            broke(board,12,13,6,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver)
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "," + str(read7) + "," + str(read8) + "," + str(read9) + "," + str(read10) + "," + str(read11) + "," + str(read12) + "\n")

"""
all broke functions analyze break of which specific wire
for loop is used to ensure power has flowed through resistors
"""
def broke(board,pinA,pinB,lead,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,server,sender,receiver):
    break1 = False
    break2 = False
    break3 = False
    for i in range(100000):
        breakRead1 = board.digital[pinA].read()
        breakRead2 = board.digital[pinB].read()
        if not breakRead1 and not breakRead2:
            break1 = True
            break2 = False
            break3 = False
            break
        if not breakRead1 and breakRead2:
            break2 = True
            break3 = False
        if breakRead1 and not breakRead2:
            break2 = False
            break3 = True
    if break1:
        print("lead "+str(lead)+" broken 1")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 1\nWire 1")
    if break2:
        print("lead "+str(lead)+" broken 2")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 1\nWire 2")
    if break3:
        print("lead "+str(lead)+" broken 3")
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead 1\nWire 3")
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "," + str(read7) + "," + str(read8) + "," + str(read9) + "," + str(read10) + "," + str(read11) + "," + str(read12) + "\n")


if __name__ == '__main__':
    init()
