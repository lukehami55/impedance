from pyfirmata import Arduino, util, INPUT
from datetime import datetime
from csv import writer

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
read_a gets first impedence reading
read_a always goes high no matter the location
"""
def read(board):
    while True:
        read_a = board.analog[0].read() 
        if read_a > 0.2: #
            broke(board) #analyze location of break
            break
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now())+","+str(read_a)+","+str(read_b)+","+str(read_c)+"\n")

                
"""
seperate function and large range used as it takes time for read_b and read_c to populate
logic flow:
read_a is known to be high
if no additional high value in range interval, break occured at break1
if read_b is high in interval, turns off break1 possibility and adds break2 possibility
if read_c is high, break can only occur at break3 ("only" is reason for "break" statement), turns off break1 and break2 possibility
"""
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
