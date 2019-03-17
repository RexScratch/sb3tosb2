SB3 to SB2 Converter
==============

A simple Python 3 program that converts .sb3 files to .sb2 files

Requirements
--------------
- Python 3 (preferably 3.6.2 or later)

Installation
--------------
Download and extract the ZIP file and move the sb3tosb2.py file to wherever you want.

Usage
--------------
1. Run sb3tosb2.py with Python
2. Select the SB3 file to open
3. Either select the SB2 file to save to or type in a new file name

Usage (command line)
--------------
1. Open the terminal or command prompt and navigate to the directory of the sb3tosb2.py file.
2. Enter the following command: `python sb3tosb2.py [args] [sb3 location] [sb2 location]` (leave `[args]` empty for default options)
3. If an error is given, make sure you entered a valid sb3 file.

Arguments
--------------
Arguments should be separated by a space.
List of arguments:
- `-c`: This enables compatibility mode. Workarounds for the following blocks will be inserted into sprites:
  - costume [number v]
  - set drag mode [ v]
  - <[] contains []?> (may experience performance loss)
  - (item # of [] in [ v]) (may experience performance loss)

Known Issues
--------------
- MP3 audio files cannot be converted
- 32-bit float WAV files may not be converted correctly
- Compatibility mode changes variable monitor labels
- Compatibility mode allows ([ v] of [ v]) to access only variables (not attributes like x position, backdrop #, etc.)
- Dragging in projects converted with compatibility mode does not have the same pen behavior as in 3.0