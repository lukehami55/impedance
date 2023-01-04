from pyfirmata import Arduino, util
from datetime import datetime
import time

"""
currently written for one lea reading
add analog pins and digital pins for more leads
"""
def init():
    board = Arduino('/dev/ttyACM0')
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    board.analog[1].enable_reporting()
    board.digital[5].write(1)
    time.sleep(3)
    print("running")
    read(board)


"""
read1 gets first impedence reading
read1 always goes high no matter the location
"""
def read(board):
    while True:
        read1 = board.analog[0].read()
        read2 = board.analog[1].read()
        if read1 < 0.2 or read2 < 0.2:
            broke(board)
        if read1 < 0.2 and read2 < 0.2:
            broke(board)
            break
        elif read1 < 0.2 and read2 > 0.2:
            broke(board)
            break
        elif read1 > 0.2 and read2 < 0.2:
            broke(board)
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "\n")


"""
future alert sms system 
"""
def broke(board):
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
        print("broken 1")
    if break2:
        print("broken 2")
    if break3:
        print("broken 3")
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "\n")


if __name__ == '__main__':
    init()
