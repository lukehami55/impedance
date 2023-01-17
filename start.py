from pyfirmata import ArduinoMega, util, INPUT, STRING_DATA
import time


def start():
    board = ArduinoMega('/dev/ttyACM0')
    board.digital[20].mode = INPUT
    it = util.Iterator(board)
    it.start()
    time.sleep(3)
    while True:
        button = board.digital[20].read()
        if button:
            print("start the program")
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Request Received"))
            break
            
            
if __name__ == '__main__':
    start()
