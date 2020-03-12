#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16
from std_msgs.msg import Bool

def callback(data):
    # print('Analog stick Values:','0',data.axes[0]) // left stick-left to right
    # print('Analog stick Values:','1',data.axes[1]) // left stick-up to down
    # print('Analog stick Values:','2',data.axes[2]) // l2 button

    # right stick-steering
    steer = int(data.axes[3]*10)

    # left stick left to right-throttle
    throttle = int((data.axes[1]+1)*50)-50
    if throttle<0: throttle=0


    # l2 and r2 button combined press for gear buttons[9] l3 buttons[10] r3
    neutral= data.buttons[0] # Button A
    forward = data.buttons[3] # Button Y
    global gearstate

    if gearstate == 2 and forward == True and neutral == False: # forward pressed, neutral -> forward
        gearstate=4
    elif gearstate == 4 and neutral == True and forward == False: # neutral pressed, forward -> neutral
        gearstate = 2
    elif gearstate == 2 and neutral == False and forward == False: # in neutral , remain in neutral
        pass
    elif gearstate == 4 and neutral == False and forward == False: # in forward, remain in forward
        pass




    brake2 = 60 - int((data.axes[5]+1)*30)
    brake1 = 60 - int((data.axes[2]+1)*30)
    brake=max(brake1,brake2)

    if brake1<10 and brake2<10:
        brake=0
    steer_pub.publish(steer)
    throt_pub.publish(throttle)
    gear_pub.publish(gearstate)
    brake_pub.publish(brake)


if __name__ == '__main__':
    rospy.init_node('Joy_node', anonymous=True)
    rospy.Subscriber("joy", Joy, callback)

    gearstate = 2
    steer_pub = rospy.Publisher('steering', Int16, queue_size=10)
    throt_pub = rospy.Publisher('throttle', Int16, queue_size=10)
    gear_pub = rospy.Publisher('gearstate', Int16, queue_size=10)
    brake_pub = rospy.Publisher('brake', Int16, queue_size=10)

    rospy.spin()
