# IMPEDANCE TESTING
A basic description of Raspberry Pi/Arduino monitoring system for lead impedance testing. Provides necessary programs and details needed to perform the monitoring system part of the impedance test.

# LEAD DIAGRAM
![Flow](https://github.com/lukehami55/impedance/blob/main/leadFlow.png?raw=true)

Diagram is for one lead, replication needed for multiple leads. 5V can be a common source across multiple lead circuits. No pinA and pinB duplications (example: if two leads are needed, there needs to be 4 total input pins).

# GETTING STARTED
## Raspberry Pi
- git clone repository
```
git clone https://github.com/lukehami55/impedance.git
```
- Installation of [pyFirmata](https://pypi.org/project/pyFirmata/)

## Arduino
- Load standardFirmataLCD.ino file onto Arduino Mega (either arduino-cli or other computer)

# RUNNING
Invoke firmata.py script on the Raspberry Pi using the following:
```
python firmata.py
```
# SCRIPT LOGIC
## Button Loop
This initial loop that the script enters:

``` python
while True:
        button = board.digital[30].read()
        if button:
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(""))
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Request Received"))
            print("Request received")
            init(board)
            break
        time.sleep(.1)
```
Script will remain in this loop till button is pressed (digital pin 30 reading is high).

## Read Loop
This is the main loop that the script enters:
``` python
while True:
        read1 = board.digital[53].read()
        read2 = board.digital[52].read()
        read3 = board.digital[51].read()
        read4 = board.digital[50].read()
        if not read1 or not read2:
            broke(board,53,52,1,read1,read2,read3,read4,server,sender,receiver)
            break
        elif not read3 or not read4:
            broke(board,51,50,2,read1,read2,read3,read4,server,sender,receiver)
        else:
            with open("output.txt", "a") as output:
                output.write(str(datetime.now()) + "," + str(read1) + "," + str(read2) + "," + str(read3) + "," + str(read4) + "\n")
```
In this example, loop has been shortened to show a 2 lead monitoring system. Read values and conditional blocks can be added or removed to add or remove the number of leads being monitored. True/False read values will be reported in output.txt.

## Break Algorithm
This is the logic used to define to the location of a break:
``` python
def broke(board,pinA,pinB,lead,read1,read2,read3,read4,server,sender,receiver):
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
```
Per lead, there are two digital inputs (pinA and pinB) used to complete the logic flow implemented in the break function:
|  | pinA    | pinA    | Result |
| :---:   | :---: | :---: | :---: |
| Read | 1   | 1   | no breaks (implemented in read loop) |
| Read | 0   | 0   | wire 1 break |
| Read | 0   | 1   | wire 2 break |
| Read | 1   | 0   | wire 3 break |

## Notifications
The following is the notification segment when a break is found:
``` python
if break1:
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("BREAK"))
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead "+str(lead)+" Wire 1"))
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead "+str(lead)+"\nWire 1")
    if break2:
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("BREAK"))
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead "+str(lead)+" Wire 2"))
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead "+str(lead)+"\nWire 2")
    if break3:
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("BREAK"))
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lead "+str(lead)+" Wire 3"))
        server.sendmail(sender, receiver, "\nLEAD BREAK:\n\nLead "+str(lead)+"\nWire 3")
```
The LCD screen is updated with break information and phone numbers added to credentials.json will receive an sms notification with break information.
