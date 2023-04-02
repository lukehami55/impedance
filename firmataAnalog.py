from pyfirmata import ArduinoMega, util, INPUT, STRING_DATA
from datetime import datetime
import smtplib
import time
import json
import requests


"""
board initialization outside of loop
"""
board = ArduinoMega('COM8')
board.digital[30].mode = INPUT
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[1].enable_reporting()
board.analog[2].enable_reporting()
board.analog[3].enable_reporting()
board.analog[4].enable_reporting()
board.analog[5].enable_reporting()
board.analog[6].enable_reporting()
board.analog[7].enable_reporting()
board.analog[8].enable_reporting()
board.analog[9].enable_reporting()
board.analog[10].enable_reporting()
board.analog[11].enable_reporting()
board.analog[12].enable_reporting()
board.analog[13].enable_reporting()
board.analog[14].enable_reporting()
board.analog[15].enable_reporting()
time.sleep(3)


def button(board):
    buttonOverride = time.time()
    while True:
        button = board.digital[30].read()
        #if button:
        if time.time() - buttonOverride > 5:
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(""))
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Request Received"))
            print("Request received")
            init(board)
            break
        time.sleep(.1)


def init(board):
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(""))
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Running"))
    print("running")
    runTime = time.time()
    read(board, runTime)


"""
main reading function
checking for any abnormalities, faster than applying entire diagnosis in this main driver function
if abnormalities are detected, moves to broke function for further diagnosis
"""
def read(board, runTime):
    while True:
        read1 = board.analog[0].read()
        read2 = board.analog[1].read()
        read3 = board.analog[2].read()
        read4 = board.analog[3].read()
        read5 = board.analog[4].read()
        read6 = board.analog[5].read()
        read7 = board.analog[6].read()
        read8 = board.analog[7].read()
        read9 = board.analog[8].read()
        read10 = board.analog[9].read()
        read11 = board.analog[10].read()
        read12 = board.analog[11].read()
        read13 = board.analog[12].read()
        read14 = board.analog[13].read()
        read15 = board.analog[14].read()
        read16 = board.analog[15].read()
        print(read1)
        if not read1 or not read2:  # if any values are false (values are normally true)
            broke(board, 0, 1, 1, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read3 or not read4:
            broke(board, 2, 3, 2, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read5 or not read6:
            broke(board, 4, 5, 3, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read7 or not read8:
            broke(board, 6, 7, 4, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read9 or not read10:
            broke(board, 8, 9, 5, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read11 or not read12:
            broke(board, 10, 11, 6, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read13 or not read14:
            broke(board, 12, 13, 7, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        elif not read15 or not read16:
            broke(board, 14, 15, 8, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16)
            break
        else:
            if time.time() - runTime > 0.025:
                runTime = time.time()
                with open("output.txt", "a") as output:
                    output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "," + str(read7) + "," + str(read8) + "," + str(read9) + "," + str(read10) + "," + str(read11) + "," + str(read12) + "," + str(read13) + "," + str(read14) + "," + str(read15) + "," + str(read16) + "\n")
            else:
                pass
"""
all broke functions analyze break of which specific wire
for loop is used to ensure power has flowed through resistors
"""
def broke(board, pinA, pinB, lead, read1, read2, read3, read4, read5, read6, read7, read8, read9, read10, read11, read12, read13, read14, read15, read16):
        break1 = False
        break2 = False
        break3 = False
        for i in range(100000):
            breakRead1 = board.analog[pinA].read()
            breakRead2 = board.analog[pinB].read()
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
        with open('credentials.json', 'r') as file:  # read in json
            credential = json.load(file)
        hook = credential["slackHook"]
        payload = {"text": "Lead " + str(lead) + " Wire "}
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("BREAK"))
        if break1:
            print("Lead " + str(lead) + " Wire 1")
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead " + str(lead) + " Wire 1"))
            payload = {"text": "Lead " + str(lead) + " Wire 1"}
        if break2:
            print("Lead " + str(lead) + " Wire 2")
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead " + str(lead) + " Wire 2"))
            payload = {"text": "Lead " + str(lead) + " Wire 2"}
        if break3:
            print("Lead " + str(lead) + " Wire 3")
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead " + str(lead) + " Wire 3"))
            payload = {"text": "Lead " + str(lead) + " Wire 3"}
        payload_json = json.dumps(payload)
        response = requests.post(hook, data=payload_json, headers={"Content-Type": "application/json"})
        print(response.status_code)
        with open("output.txt", "a") as output:
            output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "," + str(read5) + "," + str(read6) + "," + str(read7) + "," + str(read8) + "," + str(read9) + "," + str(read10) + "," + str(read11) + "," + str(read12) + "," + str(read13) + "," + str(read14) + "," + str(read15) + "," + str(read16) + "\n")
        button(board)


if __name__ == '__main__':
    button(board)
