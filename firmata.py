from pyfirmata import Arduino, util, INPUT
from datetime import datetime
from csv import writer
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
        if read1 > 0.2: #
            broke(board) #analyze location of break
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now())+","+str(read1)+","+str(read1)+","+str(read1)+"\n")

                
"""
reference "leadFlow.png" diagram
seperate function and large range used as it takes time for read2 and read3 to populate
break1 = faulty bend1
break2 = faulty bend2
break3 = faulty bend3

logic flow:
read1 is known to be high
if no additional high value in range interval, break1 is true
if read2 is high in interval, turns off break1 possibility and adds break2 possibility
if read3 is high, break can only occur at break3 ("only" is reason for "break" statement), turns off break1 and break2 possibility
"""
def broke(board):
    break1 = True
    break2 = False
    break3 = False
    for i in range(100000):
        read2 = board.analog[1].read()
        read3 = board.analog[2].read()
        if read3 > 0.2:
            break1 = False
            break2 = False
            break3 = True
            break
        if read2 > 0.2:
            break1 = False
            break2 = True
    alert(break1, break2, break3)

        
"""
future alert sms system 
"""
def alert(break1, break2, break3):
    if break1:
        print("broken first one")
    if break2:
        print("broken second one")
    if break3:
        print("broken third one")


if __name__ == '__main__':
    init()
