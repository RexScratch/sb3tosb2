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
2. Type in the following command: `python sb3tosb2.py [sb3 location] [sb2 location]`
3. If an error is given, make sure there isn't already an sb2 file at the specified location.

Known Issues
-------------
- Bitmap images in SVG files may be positioned incorrectly
- Text containing descenders in SVG files may be incorrectly positioned
- MP3 audio files cannot be converted
- 32-bit float WAV files may not be converted correctly
