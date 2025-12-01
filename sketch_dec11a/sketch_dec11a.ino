#include <Servo.h>
#include <string.h>
Servo ms_thumb_muscle, ms_thumb, ms_index, ms_middle, ms_ring, ms_pinky, s_forarm, s_elbow;
String morsecode;

void setup() {
  ms_thumb_muscle.attach(3);
  ms_thumb.attach(5);
  ms_index.attach(6);
  ms_middle.attach(9);
  ms_ring.attach(10);
  ms_pinky.attach(11);
  s_forarm.attach(2);
  s_elbow.attach(4);

  Serial.begin(9600); // Initialize serial communication
}

// Function to reset all servos to their default positions
void reset_servos() {
  ms_thumb_muscle.write(180);  // Thumb muscle to neutral
  ms_thumb.write(0);          // Thumb to neutral position
  ms_index.write(0);
  ms_middle.write(0);
  ms_ring.write(0);
  ms_pinky.write(0);
  s_forarm.write(0);
  s_elbow.write(30);
  delay(1000);
}

// Function to reset only the fingers to their default positions
void reset_fingers() {
  ms_thumb_muscle.write(180);
  ms_thumb.write(0);
  ms_index.write(0);
  ms_middle.write(0);
  ms_ring.write(0);
  ms_pinky.write(0);
  delay(1000);
}

// Function to perform a handshake gesture
void shake_hand() {
  ms_thumb_muscle.write(90);  // Adjust thumb muscle for handshake
  ms_thumb.write(90);         // Adjust thumb angle
  delay(500);
  for (int i = 0; i < 3; i++) {
    s_elbow.write(60);
    delay(500);
    s_elbow.write(20);
    delay(500);
  }
  reset_servos();
}

// Function for a "like" gesture
void like() {
  ms_index.write(160);
  ms_middle.write(160);
  ms_ring.write(160);
  ms_pinky.write(140);
  reset_servos();
}

// Function for a "dislike" gesture
void dislike() {
  ms_index.write(160);
  ms_middle.write(160);
  ms_ring.write(160);
  ms_pinky.write(140);
  s_forarm.write(0);
  reset_servos();
}


// Function for "rock" gesture
void rock() {
  ms_thumb.write(90);         // Thumb should stay neutral
  ms_index.write(160);        // Adjust these values as necessary for your setup
  ms_middle.write(160);
  ms_ring.write(160);
  ms_pinky.write(90);
}

// Function for "paper" gesture
void paper() {
  reset_fingers();
}

// Function for "scissors" gesture
void scissors() {
  ms_thumb.write(90);
  ms_ring.write(160);
  ms_pinky.write(90);
  ms_thumb_muscle.write(90);
}



// Function for a random rock-paper-scissors gesture
void rock_paper_sci() {
  rock();
  reset_fingers();
  
  int rand = random(0, 3);
  if (rand == 1) {
    rock();
  } else if (rand == 2) {
    scissors();
  } else {
    paper();
  }
  
  delay(2000);
  reset_servos();
}

// Function to point
void point() {
  s_elbow.write(45);
  ms_thumb.write(90);
  ms_middle.write(160);
  ms_ring.write(160);
  ms_pinky.write(140);
  reset_servos();
}

// Function to signal "help"
void help() {
  s_elbow.write(120);
  for (int i = 0; i < 3; i++) {
    rock();
    delay(500);
    reset_fingers();
    delay(1000);
  }
}

// Function for a peace sign gesture
void peace_sign() {
  s_elbow.write(120);
  s_forarm.write(90);
  scissors();
  delay(500);
  reset_servos();
}

// Function to simulate knocking
void knocking() {
  s_elbow.write(45);
  s_forarm.write(90);
  rock();
  for (int i = 0; i < 3; i++) {
    s_elbow.write(0);
    delay(500);
    s_elbow.write(45);
    delay(500);
  }
  reset_servos();
}

// Function to wave
void wave() {
  for (int i = 0; i < 3; i++) {
    s_elbow.write(180);
    delay(500);
    s_elbow.write(60);
    delay(500);
  }
  reset_servos();
}
void receiveAngles() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read the serial input until newline
    int angles[5];
    int prevIndex = 0, index = 0;

    // Split the input data into angles and store them in an array
    for (int i = 0; i < data.length(); i++) {
      if (data[i] == ',') {
        angles[index] = data.substring(prevIndex, i).toInt();
        prevIndex = i + 1;
        index++;
      }
    }
    angles[index] = data.substring(prevIndex).toInt();  // Last angle value

    // Update the servo positions based on received angles
    ms_thumb_muscle.write(180);
    ms_thumb.write(angles[0]);
    ms_index.write(angles[1]);
    ms_middle.write(angles[2]);
    ms_ring.write(angles[3]);
    ms_pinky.write(angles[4]);

    // Debugging: Print the received angles
    Serial.print("Received Angles: ");
    for (int i = 0; i < 5; i++) {
      Serial.print(angles[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
}

void morse(String morseCode){
  reset_fingers();
  for (int i = 0; i < morseCode.length(); i++) {
      char symbol = morseCode[i];
      Serial.print("Processing symbol: ");
      Serial.println(symbol);
      if (symbol == '.') {
        ms_index.write(90);
        delay(400);
        reset_fingers();
      } else if (symbol == '-') {
        ms_index.write(90);
        ms_middle.write(90);
        delay(800);
        reset_fingers();
      } else if (symbol == ' ') {
        reset_fingers();
        delay(400);
      } else if (symbol == '/') {
        ms_pinky.write(90);
        delay(1000);
        reset_fingers();
      }
      delay(300);
    }
}

/*
ms_thumb_muscle.attach(3);
  ms_thumb.attach(5);
  ms_index.attach(6);
  ms_middle.attach(9);
  ms_ring.attach(10);
  ms_pinky.attach(11);
  s_forarm.attach(2);
  s_elbow.attach(4);
*/
 void loop() {
  // if(Serial.available()){
  //   morsecode = Serial.readStringUntil('\n');
  //   Serial.print("Received: ");
  //   Serial.println(morsecode);
  //   morse(morsecode);


  s_elbow.write(180);
 delay(1000);
}