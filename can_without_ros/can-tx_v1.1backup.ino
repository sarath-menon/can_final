/******************************************************************************************************
* 
* message frames are set as invalid
* test only with body commands
* VERSION 0.1
* edited by JGEOB
*******************************************************************************************************/

#include <mcp_can.h>
#include <SPI.h>

MCP_CAN CAN0(53);     // Set CS to pin 53


void setup()
{
  Serial.begin(115200);
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  
  CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ);
  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted
}


//
//
//byte throt(int throtacc)                        //function to convert throttle to binary byte
//{byte acc=throtacc;
//byte valid=B1;
//byte thtot=(acc<<1)|valid;
////Serial.println("throttle:");
////Serial.println(thtot,BIN);
//return thtot;
//}



void loop()
{

//int steer=0;
//byte steerbyte = steerconv(steer);
//int throtacc=10;
////byte throtbyte = throt(throtacc);
//Serial.println(throtbyte);
byte st=0;
byte th=30; 
byte throttle[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B00110001};

byte steering[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B11000000, st};

byte horn_wiper[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B00010110};  //01101000

byte brake[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B10000000 , 0x00};  //10000000 

byte body_light[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, B10010000};  //00001001   10010000

byte gear_shift[8] = {0x00, 0x00,0x00, 0x00, 0x00, 0x00, B00100100, 0x00};

  
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
//  byte sndStat = CAN0.sendMsgBuf(0x770, 0, 8, throttle);
//  if(sndStat == CAN_OK){
//    Serial.println("Message Sent Successfully!");
// } else {
//    Serial.println("Error Sending Message...");
// }
//

CAN0.sendMsgBuf(0x770, 0, 8, throttle);
delay(1);
-
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
 
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
