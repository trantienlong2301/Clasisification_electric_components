// Định nghĩa các chân kết nối
#include <Servo.h>

Servo myServo1;  // Tạo đối tượng Servo
int curent_angle = 0;
int target_angle =0;
#define DIR_PIN 4  // Chân DIR nối với D4
#define STEP_PIN 3 // Chân STEP nối với D3
#define servo1 9 
unsigned long previousStepTime = 0; // Lư thời gian bước trước đó
unsigned long previousServoTime = 0; // Lưu thời gian cập nhật servo trước đó
unsigned long previousXungTime = 0; // Lưu thời gian bước trước đó
const int stepInterval = 65;  // Thời gian giữa các bước (micro giây)
bool stepState = HIGH;          // Trạng thái tín hiệu STEP (HIGH/LOW)
int isStepperOn = 0;
void setup() {
  Serial.begin(9600);
  myServo1.attach(servo1); // Kết nối servo vào chân số 9

  // Thiết lập các chân là OUTPUT
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);

  // Cài đặt chiều quay (HIGH: chiều thuận, LOW: chiều ngược)
  digitalWrite(DIR_PIN, LOW); // Quay theo chiều thuận
}
void servo(int a, int b){
  if (a<b){
    for (a;a<b;a++){
      myServo1.write(a);
      delay(10);
      curent_angle = target_angle;
    }
  }
  if (a>b){
    for (a;a>b;a--){
      myServo1.write(a);
      delay(10);
      curent_angle = target_angle;
    }
  }
  if (a==b){
    myServo1.write(b);
  }
  
}
void on_step(){
  unsigned long currentTime_step = micros();
  if (currentTime_step - previousStepTime >= stepInterval) {
    previousStepTime = currentTime_step;
    stepState = !stepState;
    digitalWrite(STEP_PIN, stepState);  // Tạo xung điều khiển stepper
  }
}
void off_step(){
    digitalWrite(STEP_PIN, LOW);
}
void loop() {
  String command = "";
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "ON") {
      isStepperOn = 1;
      Serial.println(isStepperOn);
    } 
    if (command == "OFF") {
      isStepperOn = 0;
      Serial.println(isStepperOn);
    }
    if (command == "0"){
      target_angle = 0;
    }
    if (command == "1"){
      target_angle = 45;
    }
    if (command == "2"){
      target_angle = 90;
    }
  }
  
  if (isStepperOn) {
    on_step();
  }
  if (!isStepperOn) {
    off_step();
  }
  servo(curent_angle, target_angle);
}
