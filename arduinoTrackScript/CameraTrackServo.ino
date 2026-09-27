#include <Servo.h>

Servo myservo;
int Frame_Res = 640;
int x , w;
int ServoPin=9;
int Centre = Frame_Res/2;
int face_centre= Frame_Res/2;;
static int ServoPos=90;

const int SERVO_MIN_ANGLE = 0;   // max angle
const int SERVO_MAX_ANGLE = 180; // min angle

//Serial stuff im copying
const int MAX_DATA_LENGTH = 64;
char receivedData[MAX_DATA_LENGTH];
int dataIndex = 0;


void setup() {
  myservo.attach(9);
  myservo.write(ServoPos);
  Serial.begin(115200);
  delay(5);
}

void loop() {
// if ant data availalbe
  if (Serial.available() > 0) {
    char incomingChar = Serial.read(); // Read one byte at a time

    // If the character is not newline terminator so data remains
    if (incomingChar != '\n') {
      // store data
      if (dataIndex < MAX_DATA_LENGTH - 1) { // Leave space for null terminator
        receivedData[dataIndex] = incomingChar;
        dataIndex++;
      } else {
        // Handle buffer
        dataIndex = 0;
        memset(receivedData, 0, MAX_DATA_LENGTH);
      }
    } else { // end line recieved end of data
      receivedData[dataIndex] = '\0'; 

      //parsing
      int numParsed = sscanf(receivedData, "%d,%d", &x, &w);

      if(numParsed==2){
        face_centre = (x+ (w/2));
        if(face_centre < Centre-100){
          ServoPos++;
        }
        else if (face_centre>Centre+100){
          ServoPos--;
        }
        ServoPos = constrain(ServoPos, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE);
        myservo.write(ServoPos);
        delay(100);
      }
      dataIndex = 0;
      memset(receivedData, 0, MAX_DATA_LENGTH); // clear buffer
    }
  }
}
