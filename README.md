# Follow-the-Dot-Robot
Constructed a robot that detects and follows 2D movement of a colored pin within a system using stepper motors, motor driver, MSP Launchpad, and a camera.

Movement of colored pin was detected using a camera with Python OpenCV running to send coordinates to the MSP Launchpad using UART communication.

A stepper motor control program written in C was flashed onto the MSP Launchpad to control the robot’s pointer based on the coordinates the Python program dictated.
