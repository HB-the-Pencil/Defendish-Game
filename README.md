# Defendish-Game
This is a clone of the arcade game Defender created in Pygame. Sprites were redrawn by hand (and the background was generated using a Khan Academy program) and based on the spritesheet found at [https://seanriddle.com/defendersprites.jpg](https://seanriddle.com/defendersprites.jpg). The project is based on Chapter 12 of the book Python Crash Course, but turned into Defender instead of Space Invaders.

## Installation

~~To run the program, download the release, open your terminal, change directories to the file, and type:~~

~~pip install -r requirements.txt~~

~~If you are using PyCharm as your editor, you can also open the terminal in the lower right corner and run the same command. PyCharm may even suggest that there is a requirement package and ask to set up the virtual environment for you.~~

You can still manually install dependencies based on the above steps, but the code now does it for you :D

There will be a build eventually so that it can run as an executable file.

# Version Notes:
## 1.0:
- Added the player and drifty movement
- Limited the player from going too high or too low
- Scaled the window

### 1.0.1 (Fancy Movement Update):
- Improved the player movement and adding smooth flipping
- Created a scrolling background and camera
- Created a space for the scanner
- Added fire particles

### 1.0.2 (Sprite Update):
- Minor bug fixes, mostly
- Imported sprite images
- Created requirements.txt

### 1.0.3 (Easy Update):
- Created main.py for easier runnning
- Wrote script to automatically import dependencies
- Began adding scanner

### 1.0.4 (Fun Update):
- Added lazers (lazer.py)
- Improved ship flip animation
- Added debug mode
- Broke code into more modular sections

### 1.0.5 (Sound Update):
- Added sound effects!!
- Added a shell for aliens (to be edited later)
- Added stars (with parallax) to the background
