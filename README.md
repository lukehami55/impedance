# Impedance Testing
A basic description of Raspberry Pi/Arduino monitoring system for lead impedance testing. Provides necessary programs and details needed to perform the monitoring system part of the impedance test.

# Lead Diagram
![Flow](https://github.com/lukehami55/impedance/blob/main/leadFlow.png?raw=true)

Variables in diagram are associated with variables found in firmata.py script. Diagram is for one lead, replication of variables needed to fulfill all ten leads. Ten leads need 30 analog inputs and 10 digital outputs.

# Getting Started
Upload the firmata.py file onto the Raspberry Pi along with the installation of the [pyFirmata](https://pypi.org/project/pyFirmata/)

# Running
Invoke firmata.py script on the Raspberry Pi using the following:
> python firmata.py
