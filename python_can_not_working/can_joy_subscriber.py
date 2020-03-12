#!/usr/bin/env python
from __future__ import print_function

import can
import time
import rospy
from std_msgs.msg import Int16

from std_msgs.msg import Bool

def steer_fn(steerdat):
    steerdata=steerdat.data
    if(steerdata < 0):
        steerdatafinal = int(bin(abs(steerdata)) + '10',2)
    elif(steerdata > 0):
        steerdatafinal = int(bin(steerdata)+ '01',2)
    else:
        steerdatafinal = int(bin(steerdata)+ '00',2)
    print('steering value',steerdat.data)
    steer = can.Message(
    arbitration_id=0x774, data=[steerdatafinal,int(bin(0b00000011),2),0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)


    bus.send(gear)
    bus.send(ind)
    bus.send(steer)
    bus.send(brake)
    bus.send(throt)
    bus.send(wipe)


def gear_fn(geardat):

    geardata=geardat.data
    # if(geardata == 1):
    #     geardatabyte = int(bin(0b00001) + '100',2)
    if(geardata == 2):
        geardatabyte = int(bin(0b00010) + '100',2)
    elif(geardata == 4):
        geardatabyte = int(bin(0b00100) + '100',2)
    print('gear  Value:',geardat.data)
    gear = can.Message(
    arbitration_id=0x778, data=[0x00, geardatabyte ,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)


    bus.send(gear)
    bus.send(ind)
    bus.send(steer)
    bus.send(brake)
    bus.send(throt)
    bus.send(wipe)

def throttle_fn(throtdat):
    throtdata=throtdat.data
    print('throttle  Value:',throtdat.data)
    throtdatafinal = int(bin(throtdata) + '1',2)
    throt = can.Message(
    arbitration_id=0x770, data=[throtdatafinal,0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    bus.send(gear)
    bus.send(ind)
    bus.send(steer)
    bus.send(brake)
    bus.send(throt)
    bus.send(wipe)

def brake_fn(brakedat):
    brakedata=brakedat.data
    print('brake Value:',brakedat.data)
    brakedatafinal = int(bin(brakedata) + '1',2)
    brake = can.Message(
    arbitration_id=0x772, data=[brakedatafinal,0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    bus.send(gear)
    bus.send(ind)
    bus.send(steer)
    bus.send(brake)
    bus.send(throt)
    bus.send(wipe)


if __name__ == '__main__':
    try:
        bus = can.interface.Bus(bustype='virtual', channel='can0', bitrate=500000)
        rospy.init_node('can_2', anonymous=True)

        throt = can.Message(
        arbitration_id=0x770, data=[int(bin(0b00000001),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

        gear = can.Message(
        arbitration_id=0x778, data=[0x00, int(bin(0b00010100),2) ,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

        steer = can.Message(
        arbitration_id=0x774, data=[0x00,int(bin(0b00000011),2),0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

        brake = can.Message(
        arbitration_id=0x772, data=[int(bin(0b00000001),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

        ind = can.Message(
        arbitration_id=0x776, data=[int(bin(0b00001001),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

        wipe = can.Message(
        arbitration_id=0x76D, data=[int(bin(0b00101000),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

        steer_sub = rospy.Subscriber("steering", Int16, steer_fn)
        throttle_sub = rospy.Subscriber("throttle", Int16, throttle_fn)
        gear_sub = rospy.Subscriber("gearstate", Int16, gear_fn)
        brake_sub = rospy.Subscriber("brake",Int16,brake_fn)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
