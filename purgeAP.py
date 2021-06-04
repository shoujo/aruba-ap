import serial
import sys
from time import sleep
from pexpect import *
from pexpect_serial import SerialSpawn


def spawnSerial(ap_model, baud):
    return serial.Serial(ap_model, baud, timeout=300)
    

def sendAPCommands(child):
    commands = [
        'purgeenv',
        'saveenv',
        'printenv'
        ]
    for command in commands:
        child.sendline(command)
        child.expect('\r\napboot> ')
    return child.close()


def createAPChild(child):
    child.logfile_read = sys.stdout
    while child:
        child.delaybeforesend = None
        pattern_list = ['autoboot:', '\r\napboot> ']
        i = child.expect_exact(pattern_list, timeout=None)
        if i == 0:
            child.sendline('')
        if i == 1:
            sendAPCommands(child)
    
        
def connectAP225():
    ap_serial = '/dev/cu.usbserial-AI043YB9'
    baud = 9600
    with spawnSerial(ap_serial, baud) as ser:
        try:
            child = SerialSpawn(ser, encoding='utf-8')
            createAPChild(child)
        except:
            pass    
    print("SUCCESS: AP Purge Complete!")
        

def main():
    connectAP225()
    
    
if __name__ == "__main__":
    main()    
