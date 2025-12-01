#include <Servo.h> 

//defining all the 8 servos 
Servo ms_thumb_muscle,ms_thumb,ms_index,ms_middle,ms_ring,ms_pinky,s_forarm,s_elbow;

void setup() {
  ms_thumb_muscle.attach(11);
  ms_thumb.attach(3);
  ms_index.attach(5);
  ms_middle.attach(6);
  ms_ring.attach(9);
  ms_pinky.attach(10);
  s_forarm.attach(2);
  
}

void reset_servos()
{
  //this function resets all the servos 
  delay(1000);
  if (ms_thumb_muscle.read() != 0) {
    ms_thumb_muscle.write(0);
  }
  if (ms_thumb.read() != 0) {
    ms_thumb.write(0);
  }
  if (ms_index.read() != 0) {
    ms_index.write(0);
  }
  if (ms_middle.read() != 0) {
    ms_middle.write(0);
  }
  if (ms_ring.read() != 0) {
    ms_ring.write(0);
  }
  if (ms_pinky.read() != 0) {
    ms_pinky.write(0);
  }
  if (s_forarm.read() != 0) {
    s_forarm.write(0);
  }
  if (s_elbow.read() != 30) {
    s_elbow.write(30);
  }
  delay(1000);
}

void reset_fingers()
{
  //this function resets all the finger servos
  delay(1000);
  if (ms_thumb_muscle.read() != 0) {
    ms_thumb_muscle.write(0);
  }
  if (ms_thumb.read() != 0) {
    ms_thumb.write(0);
  }
  if (ms_index.read() != 0) {
    ms_index.write(0);
  }
  if (ms_middle.read() != 0) {
    ms_middle.write(0);
  }
  if (ms_ring.read() != 0) {
    ms_ring.write(0);
  }
  if (ms_pinky.read() != 0) {
    ms_pinky.write(0);
  }
  delay(1000);
}

void shake_hand()
{
  //this function shake hand  
  ms_thumb_muscle.write(90);
  ms_thumb.write(30); //adjust to the thumb angles 
  delay(500);
  for (int i = 0;i < 3;i++)
  {
    s_elbow.write(60);
    delay(1000);
    s_elbow.write(20);
    delay(1000);
  }
  reset_servos();
}

void like()
{
  //this function to make the hand do a like sign 
  //adjust all angles
  ms_index.write(30); 
  ms_middle.write(30);
  ms_ring.write(30);
  ms_pinky.write(30);
  reset_servos();
}

void dislike()
{
  //this function to make the hand do a dislike sign 
  //adjust all angles
  ms_index.write(30); 
  ms_middle.write(30);
  ms_ring.write(30);
  ms_pinky.write(30);
  s_forarm.write(180);
  reset_servos();
}

void rock()
{
  //this function to make the rock sign in rock paper scissors
  ms_thumb.write(30);
  ms_index.write(30); 
  ms_middle.write(30);
  ms_ring.write(30);
  ms_pinky.write(30);
  reset_servos();
}

void paper()
{
  //the paper sign in rock paper scissors 
  reset_fingers();
}

void scissors()
{
  //the scissors sign in rock paper scissors
  ms_thumb.write(30);
  ms_ring.write(30);
  ms_pinky.write(30);
  reset_servos();
}

void rock_paper_sci()
{
  //to choose a random between the 3 signs 
  rock();
  for (int i = 0;i < 3;i++)
  {
    s_elbow.write(90);
    delay(500);
    s_elbow.write(45);
    delay(500);
  }
  //random between rock paper scissors
  reset_servos();
}

void point()
{
  //to point to smth
  s_elbow.write(45);
  ms_thumb.write(30);
  ms_middle.write(30);
  ms_ring.write(30);
  ms_pinky.write(30);
  reset_servos();
}

void help()
{
  //help sign 
  s_elbow.write(120);
  for(int i = 0;i < 3; i++){
    rock();
    delay(500);
    reset_fingers();
  }
}

void peace_sign()
{
  //make a peace sign with ur hand
  s_elbow.write(120);
  s_forarm.write(30);
  scissors();
  reset_servos();
}

void knocking()
{
  //knocking on smth below
  s_elbow.write(45);
  s_forarm.write(30);
  rock();
  for(int i = 0;i < 3; i++)
  {
    s_elbow.write(0);
    delay(500);
    s_elbow.write(45);
    delay(500);
  }
  reset_servos();
}

void wave()
{
  //waving to someone 
  for(int i = 0; i < 3; i++){
  s_elbow.write(180);
  delay(500);
  s_elbow.write(60);
  delay(500);
  }
  reset_servos();
}
void loop() 
{
 
  s_forarm.write(0);
  delay(500);
  
 
}