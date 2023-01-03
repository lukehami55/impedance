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
    board.analog[2].enable_reporting()
    board.digital[5].write(1)
    board.digital[6].write(1)
    board.digital[7].write(1)
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
        read3 = board.analog[2].read()
        if read1 > 0.2:
            broke(board,read1,read2,read3,1)
            break
        elif read2 > 0.2:
            broke(board,read1,read2,read3,2)
            break
        elif read3 > 0.2:
            broke(board,read1,read2,read3,3)
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "\n")

"""
future alert sms system 
"""
def broke(board,read1,read2,read3,lead):
    print("broken lead "+str(lead))
    with open("output.txt", "a") as output:
        output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "\n")


if __name__ == '__main__':
    init()
