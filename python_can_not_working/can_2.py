
from __future__ import print_function

import can
import time
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Bool

def send_one():
    steerdata = rospy.wait_for_message("steering", Int16,timeout=50)
    steerdata = steerdata.data
    if(steerdata < 0):
        steerdatafinal = int(bin(abs(steerdata)) + '10',2)
    elif(steerdata > 0):
        steerdatafinal = int(bin(steerdata)+ '01',2)
    else:
        steerdatafinal = int(bin(steerdata)+ '00',2)
    # print('steering value',steerdata)


    # geardata = rospy.wait_for_message('gear', Int16, timeout=5)
    # geardata = geardata.data



    # if(geardata == 1):
    #     geardatabyte = int(bin(0b00001) + '100',2)
    # elif(geardata == 2):
    #     geardatabyte = int(bin(0b00010) + '100',2)
    # elif(geardata == 4):
    #     geardatabyte = int(bin(0b00100) + '100',2)
    # print('gear  Value:',geardata.data)



    throtdata = rospy.wait_for_message('throttle', Int16, timeout=50)
    throtdata = throtdata.data
    print('throttle  Value:',throtdata)
    throtdatafinal = int(bin(throtdata) + '1',2)


    # gear = can.Message(
    # arbitration_id=0x778, data=[0x00, geardatabyte ,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    ind = can.Message(
    arbitration_id=0x776, data=[int(bin(0b00001001),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    steer = can.Message(
    arbitration_id=0x774, data=[steerdatafinal,int(bin(0b00000011),2),0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    brake = can.Message(
    arbitration_id=0x772, data=[int(bin(0b00000001),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    throt = can.Message(
    arbitration_id=0x770, data=[throtdatafinal,0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

    wipe = can.Message(
    arbitration_id=0x76D, data=[int(bin(0b00101000),2),0x00,0x00,0x00,0x00,0x00,0x00, 0x00 ], is_extended_id=False)

if __name__ == "__main__":
    rospy.init_node('can_sender', anonymous=True)
    bus = can.interface.Bus(bustype='virtual', channel='can0', bitrate=500000)
    try:
        while True:
            send_one()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
