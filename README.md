# Attendance-System
This project presents a monitor for attendance working with a RFID module which reads information encoded on a RFID tag and opens solenoid lock if RFID tag is correct.

# Instructions:
- Extract folders and open it in IDE;
- Assemble the components just like in the schematic;
- Change the server address in read.py;
- Change the Flask server address in app.py;

# To run the main app:
python3 main.py

# To run the Flask web server:
python3 app.py

Note: Those two python programs are designed to work independently of each other. 
The main app will continue to run even if the server isn't launched, prompting an error if the POST request was unsuccessful. 
The same principle applies to the server.
