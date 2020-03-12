/******************************************************************************************************
* 
* message frames are set as invalid
* test only with body commands
* VERSION 0.1
* edited by JGEOB
*******************************************************************************************************/

#include <mcp_can.h>
#include <SPI.h>

#include <ros.h>
#include <std_msgs/Int16.h>

MCP_CAN CAN0(53); // Set CS to pin 53

ros::NodeHandle nh;


byte steerbyte;byte throtbyte;
byte gearbyte;byte brakebyte;

void steerconv( const std_msgs::Int16& steerangle)           //function to convert steerangle to binary byte
{ 
byte steer = abs(steerangle.data);
// byte steer=-5;
byte dr=B10;
byte dl=B01;


if(steerangle.data < 0) 
{
  steerbyte = (steer<<2)|dr;
}
else if(steerangle.data > 0)  
{
  steerbyte = (steer<<2)|dl;
}
else if(steerangle.data == 0 )
{
  steerbyte = (steer<<2)|dl;
}

//Serial.println("steering:");
//Serial.print(tot,BIN);

Serial.println(steerangle.data);

}


void throt( const std_msgs::Int16& throtacc)      
{
  byte acc=throtacc.data;
  byte valid=B1;
  byte thtot=(acc<<1)|valid;
//Serial.println("throttle:");
//Serial.println(thtot,BIN);
  throtbyte = thtot;
}

void brakeconv( const std_msgs::Int16& braketemp)      
{
  byte bra=braketemp.data;
  byte valid=B1;
  byte brak=(bra<<1)|valid;
//Serial.println("throttle:");
//Serial.println(thtot,BIN);
  brakebyte = brak;
}


void gearconv( const std_msgs::Int16& geartemp)      
{

if(geartemp.data == 2)
{
  byte gr=geartemp.data;
  byte valid=B100;
  byte gra=(gr<<3)|valid;
  gearbyte = gra;
}
if(geartemp.data == 4)
{
  byte gr=geartemp.data;
  byte valid=B100;
  byte gra=(gr<<3)|valid;
  gearbyte = gra;
}
}



ros::Subscriber<std_msgs::Int16> steer_sub("steering", &steerconv );
ros::Subscriber<std_msgs::Int16> throt_sub("throttle", &throt );
ros::Subscriber<std_msgs::Int16> gear_sub("brake", &brakeconv );
ros::Subscriber<std_msgs::Int16> brake_sub("gearstate", &gearconv );



void setup()
{
  
  nh.initNode();
  nh.subscribe(steer_sub);
//  nh.subscribe(brake);
  nh.subscribe(throt_sub);
//  nh.subscribe(gearstate);
  nh.subscribe(gear_sub);
  nh.subscribe(brake_sub);
  Serial.begin(57600);
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  
  CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ);
  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted
}



void loop()
{

byte throttle[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, throtbyte}; // B00110001 

byte steering[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B11000000, steerbyte};

byte horn_wiper[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B00010110};  //01101000

byte brake[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, brakebyte};  //10000000 

byte body_light[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B10010000};  //00001001   10010000

byte gear_shift[8] = {0x00, 0x00,0x00, 0x00, 0x00, 0x00, gearbyte, 0x00};

  
   //send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  byte sndStat = CAN0.sendMsgBuf(0x770, 0, 8, throttle);
  if(sndStat == CAN_OK){
//    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }


CAN0.sendMsgBuf(0x770, 0, 8, throttle);
delay(1);

CAN0.sendMsgBuf(0x772, 0, 8, brake);
delay(1);

CAN0.sendMsgBuf(0x774, 0, 8, steering);
delay(1);


CAN0.sendMsgBuf(0x776, 0, 8, body_light);
delay(1);

CAN0.sendMsgBuf(0x778, 0, 8, gear_shift);
delay(1);

CAN0.sendMsgBuf(0x76D, 0, 8, horn_wiper);
delay(1);

nh.spinOnce();
delay(1);
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
