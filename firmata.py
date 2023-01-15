from pyfirmata import Arduino, util, INPUT, STRING_DATA
from datetime import datetime
import smtplib
import time
import json


"""
10 lead setup
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
    board.digital[53].mode = INPUT
    board.digital[52].mode = INPUT
    board.digital[51].mode = INPUT
    board.digital[50].mode = INPUT
    board.digital[49].mode = INPUT
    board.digital[48].mode = INPUT
    board.digital[47].mode = INPUT
    board.digital[46].mode = INPUT
    board.digital[45].mode = INPUT
    board.digital[44].mode = INPUT
    board.digital[43].mode = INPUT
    board.digital[42].mode = INPUT
    board.digital[41].mode = INPUT
    board.digital[40].mode = INPUT
    board.digital[39].mode = INPUT
    board.digital[38].mode = INPUT
    board.digital[37].mode = INPUT
    board.digital[36].mode = INPUT
    board.digital[35].mode = INPUT
    board.digital[34].mode = INPUT
    it = util.Iterator(board)
    it.start()
    time.sleep(3)
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Running"))
    print("running")
    read(board,server,sender,receiver)


"""
main reading function
checking for any abnormalities, faster than applying entire diagnosis in this main driver function
if abnormalities are detected, moves to broke function for further diagnosis
"""
def read(board,server,sender,receiver):
    while True:
        read1 = board.digital[53].read()
        read2 = board.digital[52].read()
        read3 = board.digital[51].read()
        read4 = board.digital[50].read()
        read5 = board.digital[49].read()
        read6 = board.digital[48].read()
        read7 = board.digital[47].read()
        read8 = board.digital[46].read()
        read9 = board.digital[45].read()
        read10 = board.digital[44].read()
        read11 = board.digital[43].read()
        read12 = board.digital[42].read()
        read13 = board.digital[41].read()
        read14 = board.digital[40].read()
        read15 = board.digital[39].read()
        read16 = board.digital[38].read()
        read17 = board.digital[37].read()
        read18 = board.digital[36].read()
        read19 = board.digital[35].read()
        read20 = board.digital[34].read()
        if not read1 or not read2: #if any values are false (values are normally true)
            broke(board,reportBoard,53,52,1,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read3 or not read4:
            broke(board,reportBoard,51,50,2,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read5 or not read6:
            broke(board,reportBoard,49,48,3,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read7 or not read8:
            broke(board,reportBoard,47,46,4,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read9 or not read10:
            broke(board,reportBoard,45,44,5,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read11 or not read12:
            broke(board,reportBoard,43,42,6,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read13 or not read14:
            broke(board,reportBoard,41,40,7,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read15 or not read16:
            broke(board,reportBoard,39,38,8,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read17 or not read18:
            broke(board,reportBoard,37,36,9,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        elif not read19 or not read20:
            broke(board,reportBoard,35,34,10,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver)
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "," + str(read7) + "," + str(read8) + "," + str(read9) + "," + str(read10) + "," + str(read11) + "," + str(read12) + "," + str(read13) + "," + str(read14) + "," + str(read15) + "," + str(read16) + "," + str(read17) + "," + str(read18) + "," + str(read19) + "," + str(read20) + "\n")

"""
all broke functions analyze break of which specific wire
for loop is used to ensure power has flowed through resistors
"""
def broke(board,reportBoard,pinA,pinB,lead,read1,read2,read3,read4,read5,read6,read7,read8,read9,read10,read11,read12,read13,read14,read15,read16,read17,read18,read19,read20,server,sender,receiver):
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
        print("Lead "+str(lead)+" Wire 1")
        reportBoard.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead "+str(lead)+" Wire 1"))
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead "+str(lead)+"\nWire 1")
    if break2:
        print("Lead "+str(lead)+" Wire 2")
        reportBoard.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead "+str(lead)+" Wire 2"))
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead "+str(lead)+"\nWire 2")
    if break3:
        print("Lead "+str(lead)+" Wire 3")
        reportBoard.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead "+str(lead)+" Wire 3"))
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead "+str(lead)+"\nWire 3")
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "," + str(read7) + "," + str(read8) + "," + str(read9) + "," + str(read10) + "," + str(read11) + "," + str(read12) + "," + str(read13) + "," + str(read14) + "," + str(read15) + "," + str(read16) + "," + str(read17) + "," + str(read18) + "," + str(read19) + "," + str(read20) + "\n")


if __name__ == '__main__':
    init()
