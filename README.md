# Multi-Functional Humanoid Arm Control System

Welcome to the **Multi-Functional Humanoid Arm System** — a smart, multi-mode control application built using **Python (Tkinter)** and **Arduino** to operate a robotic humanoid arm.  
This system provides advanced interaction modes such as **Morse Code translation**, **hand-pose control**, **voice-to-text command input**, and **game modules**, all through a clean, modern GUI interface.
Video in LinkedIn (https://www.linkedin.com/posts/yousef-ibrahem1_robotics-innovation-technology-activity-7277648617102860288-nr0K?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD9UNawBC4ow4-vDQR6JMVmg4FvksSqmBoU)

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Architecture](#architecture)  
3. [Technology Stack](#technology-stack)  
4. [Project Structure](#project-structure)  
5. [Features](#features)  
6. [Getting Started](#getting-started)  
7. [Configuration](#configuration)  
8. [Modules](#modules)  
9. [Data Flow](#data-flow)  
10. [Arduino Communication](#arduino-communication)  
11. [Business Rules](#business-rules)  
12. [Error Handling](#error-handling)  
13. [Testing](#testing)  
14. [Support](#support)

---

## Project Overview

The **Humanoid Arm Control System** is a Tkinter-powered GUI designed to communicate with an Arduino-controlled robotic arm.  
The system enables users to operate the arm through:

- Morse-Code-based movements  
- Pre-defined hand poses  
- Voice-activated text commands  
- Utility and playful game modes  

The GUI is built with a clean, dark-mode interface and integrates Vosk speech recognition, serial communication, and dynamic widgets.

### Key Capabilities:

- **Arduino Serial Communication** (COM port control)  
- **Morse Code Translation → Arm Movement**  
- **Hand Pose Selector (Preset Angles)**  
- **Speech-to-Text With Vosk Model**  
- **Games and Utility Add-ons**  
- **Modern Dark UI (sv_ttk + custom title bar)**  
- **Thread-safe data sending & receiving**

---

## Architecture

The project follows a **modular, multi-screen architecture** with clear separation between:

### 1. GUI Layer (Tkinter)
- All windows, forms, widgets  
- Navigation between Main / Morse / Poses / Games  
- Dark mode styling  
- Error handling and pop-ups  

### 2. Serial Communication Layer
- Controls all Arduino communication  
- Thread-safe read/write  
- Connect/Disconnect logic  

### 3. Speech Recognition Layer
- Vosk offline speech recognition  
- Converts WAV → Text → Morse  
- Handles noise reduction  

### 4. Logic Layer
- Morse conversion  
- Pose mappings  
- Audio processing  
- Data formatting

---

## Technology Stack

### Core Technologies:
- **Python 3.10+**  
- **Tkinter GUI**  
- **Arduino + PySerial**  
- **Vosk Speech Recognition**  
- **Pyaudio / SpeechRecognition**  
- **sv_ttk for modern themes**

### Tools:
- Threading  
- WAV stream processor  
- Windows title bar styling  
- Serial locking mechanism  

---

## Project Structure
project_root/
│
├── Arm_Gui_v4.py # Main application (GUI + logic + communication)
├── Arduino/ # Arduino sketches (.ino)
├── VoskModel/ # Offline speech recognition model
└── README.md # Documentation

---

## Features

### 1. Arduino Connection Manager
- Connect / Disconnect  
- Countdown during initialization  
- Live status display  
- Pop-up notifications  

### 2. Morse Code Converter
- Convert typed text  
- Convert voice → text → Morse  
- Send Morse symbols to Arduino  
- Clean output fields  
- Supports real-time detection  

### 3. Hand Pose Controller
- Multiple robot-hand poses:
  - Touch & Hold  
  - Peace  
  - Thumbs Up  
  - Gun  
- Servo angle mapping  
- Reset to default pose  

### 4. Games Module
- Expandable game structure  
- GUI-ready mini-games  

### 5. Modern UI
- Dark theme  
- Adaptive title bar  
- Elegant widgets and buttons  

---

## Getting Started

### Prerequisites
- Python 3.10+  
- Arduino IDE  
- Vosk Model installed locally  
- USB cable + COM port  
- Required Python packages:

```bash
pip install pyserial vosk sv-ttk pyaudio SpeechRecognition pywinstyles
```

##  Steps to Run

1.  **Upload Arduino Code**: Ensure the necessary Arduino code for controlling the servo motors is uploaded to the Arduino board.
2.  **Download and place Vosk Model**: Download the required **Vosk speech recognition model** and place the model folder in the specified directory.
    * **Default Location:** `C:\robotic_arm\`
3.  **Run the Application**: Execute the main Python script from the command line.
    * **Command:** `python Arm_Gui_v4.py`
4.  **Connect to Arduino**: Use the GUI to establish a serial connection.
5.  **Start using Morse, Poses, or Games**.

---

##  Configuration

The configuration settings define how the application connects to the hardware and accesses external resources.

### Serial Port Settings
| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| `port` | `'COM5'` | The serial port where the Arduino is connected. |
| `baudrate` | `9600` | The communication speed for the serial connection. |

### Vosk Model Path
| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| `voice_model_location` | `"C:\\robotic_arm"` | The absolute path to the directory containing the Vosk model folder. |

> **Note:** You may change these paths in the source code as needed to match your setup.

---

##  Modules

The application is structured into the following functional modules:

### 1. Main Page
* **Connect/Disconnect** functionality for the serial port.
* **Navigation buttons** to switch between different control modes (Morse, Poses, Games).
* **Status indicator** to show the current connection state (e.g., Connected/Disconnected).

### 2. Morse Code Module
* **Text → Morse**: Converts user-typed text input into Morse code signals.
* **Voice → text → Morse**: Uses speech recognition (Vosk) to convert spoken words into text, and then into Morse code.
* **Clear fields** for input and output areas.
* **Send to Arduino** button to transmit the generated Morse data.

### 3. Pose Module
* **Dropdown pose selector** for choosing predefined hand positions.
* **Predefined angle sets** for each pose (specific servo motor angles).
* **Reset button** to return the arm to a neutral or default position.

### 4. Games Module
* **Placeholder** for future feature integration (e.g., simple interactive control games).

---

##  Data Flow

GUI (Tkinter)
      ↓
User Input (Text / Voice / Buttons)
      ↓
Logic Processing (Morse / Poses)
      ↓
Serial Communication Layer
      ↓
Arduino (Servo motors)

##  Arduino Communication

This section details how the Python application interacts with the Arduino board over a serial connection. 

### Sending Data

* **Method:** `serial_connection.write(data.encode())`
* **Description:** The application takes the command data (typically a string) and uses the **`.encode()`** method to convert it into a stream of **bytes** (e.g., ASCII or UTF-8), which is the format required for transmission over the serial port.

### Reading Data

* **Method:** `serial_connection.readline().decode().strip()`
* **Description:**
    * **`.readline()`**: Reads a line of incoming bytes from the Arduino, usually terminating at a newline character.
    * **`.decode()`**: Converts the received stream of bytes back into a readable **string**.
    * **`.strip()`**: Removes any leading or trailing whitespace characters (like newlines or carriage returns) to ensure clean data processing.

### Concurrency

* **Thread-safe**: All serial operations are specifically designed to be safe when the application uses **background threads** (e.g., for continuous listening or concurrent tasks).
* **Locked via `serial_lock`**: A **threading lock** mechanism is employed to ensure that only **one thread** can access and manipulate the serial port connection at any given time, preventing data corruption or race conditions.
* **Clean connection errors handled gracefully.**

---

##  Business Rules

The application operates under the following essential operational constraints and rules:

| Rule Category | Constraint | Description |
| :--- | :--- | :--- |
| **Connection Prerequisite** | **Arduino must be connected** | Data cannot be sent (Morse or Pose commands) until a successful serial connection is established. |
| **Vosk Model Requirement** | **Model folder must exist** | The Vosk model directory must be correctly placed at the configured path for the voice recognition feature to function. |
| **Input Validation** | **Empty input is not processed** | The Morse and Pose modules will ignore submissions if the input fields are blank. |
| **Pose Format** | **Pose angles must follow predefined formats** | Control data must adhere to a specific structure (e.g., a required sequence and valid range of values) for the Arduino to correctly parse and execute the movement. |
| **Audio Limits** | **Audio recording has timeout & phrase limits** | Time and phrase length restrictions are applied to audio input to prevent infinite listening or excessive processing loads. |

---

##  Error Handling

Robust error management is implemented to provide a stable user experience:

* **Missing Vosk model**: Triggers an **error popup notification** to inform the user that the voice recognition system cannot initialize.
* **COM port failure**: Triggers an **error popup** if the specified serial port cannot be opened or if the connection fails unexpectedly during use.
* **Audio timeout**: The system handles the timeout safely to stop the recording process and prevent the application from hanging.
* **Unexpected exceptions**: Any other unforeseen errors are **displayed to the user** for better debugging and reporting.

---

##  Testing 

### Manual Tests:

The following core functionalities require manual verification:

* Verify the ability to **Connect to Arduino**.
* Test successful **Send Morse code commands** (checking both text-to-Morse and voice-to-Morse workflows).
* Validate **Use Speech recognition** to ensure accurate voice-to-text conversion.
* Confirm the robotic arm correctly responds to **Change hand poses**.
* Check **disconnect logic** to ensure the serial port is properly closed and released.
* Test the error handling by intentionally trying an **invalid COM port**.

### Future Enhancements:

* Add **games functionality** to the Games Module.
* Implement **gesture-based control** (e.g., using a sensor or external controller).
* Integrate **Camera-based movement tracking** for advanced control.
* Develop **Unit tests** for core logic components to ensure code quality and stability.

---

##  Support

If the application is not functioning as expected, use this checklist for troubleshooting:

1.  Confirm the correct **COM port** (e.g., `COM5`) is specified in the configuration.
2.  **Reconnect the Arduino** physically and try re-establishing the serial connection in the GUI.
3.  Ensure all necessary **Python packages** (e.g., `pyserial`, `vosk`, `tkinter`) are installed in the environment.
4.  Confirm the **Vosk model directory path** is correct and the model files are present.
5.  **Restart the app** as a final step to clear any transient issues.
