from __future__ import print_function
import can
import time

def send_one():

    steerdata=1
    if(steerdata < 0):
        steerdatafinal = int(bin(abs(steerdata)) + '10',2)
    elif(steerdata > 0):
        steerdatafinal = int(bin(steerdata)+ '01',2)
    else:
        steerdatafinal = int(bin(steerdata)+ '00',2)

    geardata=4
    if(geardata == 1):
        geardatabyte = int(bin(0b00001) + '100',2)
    elif(geardata == 2):
        geardatabyte = int(bin(0b00010) + '100',2)
    elif(geardata == 4):
        geardatabyte = int(bin(0b00100) + '100',2)

    throtdata=10
    throtdatafinal = int(bin(throtdata) + '1',2)
    byte trot = throtdata


    gear = can.Message(
    arbitration_id=0x778, data=[0x00 ,0x00,0x00,0x00,0x00,0x00, geardatabyte,0x00  ], is_extended_id=False)

    ind = can.Message(
    arbitration_id=0x776, data=[0x00,0x00,0x00,0x00,0x00,0x00, 0x00,int(bin(0b00001001),2) ], is_extended_id=False)

    steer = can.Message(
    arbitration_id=0x774, data=[0x00,0x00,0x00,0x00,0x00, 0x00,int(bin(0b11000000),2),steerdatafinal ], is_extended_id=False)

    brake = can.Message(
    arbitration_id=0x772, data=[0x00,0x00,0x00,0x00,0x00,0x00,int(bin(0b10000000),2), 0x00 ], is_extended_id=False)

    throt = can.Message(
    arbitration_id=0x770, data=[0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ,throtdatafinal], is_extended_id=False)

    wipe = can.Message(
    arbitration_id=0x76D, data=[0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ,int(bin(0b0010110),2)], is_extended_id=False)


    bus.send(gear)
    bus.send(ind)
    bus.send(steer)
    bus.send(brake)
    bus.send(throt)
    bus.send(wipe)
    bus.flush_tx_buffer()

if __name__ == "__main__":
    bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)
    while True:
        send_one()
        print("Message sent on {}".format(bus.channel_info))
