from pyfirmata import Arduino, util, INPUT
from datetime import datetime
from csv import writer

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
    read(board)

def read(board):
    while True:
        read_a = board.analog[0].read() #read_a always gets an impedence reading before the others
        if read_a > 0.2:
            broke(board) #analysis location of break
            break
        else:
            print("nothing is broken")
            with open("test.txt", "a") as output:
                output.write(str(datetime.now())+","+str(read_a)+"\n")


def broke(board):
    break1 = True
    break2 = False
    break3 = False
    for i in range(100000):
        if board.analog[2].read() > 0.2:
            break1 = False
            break2 = False
            break3 = True
            break
        if board.analog[1].read() > 0.2:
            break1 = False
            break2 = True
        alert(break1, break2, break3)

        
def alert(break1, break2, break3):
    if break1:
        print("broken first one")
    if break2:
        print("broken second one")
    if break3:
        print("broken third one")


if __name__ == '__main__':
        init()
