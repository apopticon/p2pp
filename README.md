# p2pp - **Palette2 Post Processing tool for PrusaSlicer/Slic3r PE**

Starting with version 6.0.0 P2PP has undergone significant changes.  The tool is now available as a windows' application ZIP file or, a macOS' DMG file. from the [following location](https://www.dropbox.com/sh/q0vhg6u90a8wbox/AAB2jEGWGZBYlqXnTCLkojCla?dl=0) (under development/macOS of development/Windows folder)
You have to download the file with the latest version onto your computer and either unzip it to the location of your choice on a Windows machine or open the DMG and move the application ofver to the Applications folder on macOS.

The new file comes with a python version, including all required libraries in a single distribution.   This should make P2PP imune for changes to the Python enviromnment on your computer or installation of other versions of the needed libraries

Downside is that the new files have grown quite a bit bigger...



**Tested with version PrusaSlicer 2.3.0/2.2.0/2.1.0**
earlier versions may generate different code patterns and may not work correctly

## Purpose

Allow Palette 2 users to exploit all features and functionality of the palette 2 (Pro) with the Slic3r PE functionality for multi material printing including:

- use of variable layers without bloating the wipe tower
- wipe to waste object
- wipe to infill
- configurable option to create more filament at the end of the print 
- configurable tower print speeds
- added support for other hardware like the BifBrain3d side wipe device


**BEFORE YOU START:**

p2pp is an independently developed post processing script designed to allow Palette+/2/pro/s users the abiltiy to use Prusaslicer's advanced features nativlely directly from Prusaslicer. We test features before releasing but please understand you use this script at your own risk. We are not responsible for any damage caused.

**IMPORTANT:**
> P2PP currently is optimized for devices in a connected setup.  It is possible to generate files or the Plette+ and P2 in connected mode.  
This feature is considered ALPHA development and needs further testing


## Functionality

p2pp is a python script with a shell script/batch file wrapper.

It works as a post processor to GCode files generated by PrusaSlicer 2.1+, just like Chroma does.   If does however not create any new code for wipe towers etc, it just adds Palette 2 MCF information codes to the file.  The script is triggered automatically when exporting GCode or when sending information to the printer so no manual additional step is required.  

**IMPORTANT**
> Before using p2pp, it is imperative that you set up the printer and Palette device according to the
instructions given by Mosaic. In particular, be sure you have calibrated your printer's extruder before setting
up the Palette.
(General instructions for that can be found [here](https://all3dp.com/2/extruder-calibration-6-easy-steps-2).)
Once you have completed an initial print through CANVAS or Chroma (be sure to keep the extrusion rate at 100% 
during the initial calibration!), follow the guide(s) below and create a new 
Printer profile in PrusaSlicer. You need a separate profile because
p2pp and Chroma use different PrusaSlicer settings.

If you are new to printing with PrusaSlicer, make sure you have the printer dialed in using single filament prints before
adding the complexity of p2pp post scripting.   It will greatly simplify the debugging if you know the print, filament and printer
settings are properly tuned to work with your 3d Printer hardware.

## General information

Kurt made a video describing the installation process p2pp on a Windows system.  Besides the windows specific part this video also contains the 
setup instructions for Slic3r/PrusaSlicer and a full example on how p2pp is used.   The video can be found on YouTube:

[![youtube video](https://img.youtube.com/vi/JuTdq-IlRj4/0.jpg)](https://www.youtube.com/watch?v=JuTdq-IlRj4&t=1s "P2PP Installation and Configuration")

Some of the advanced features are not covered in this video so make sure to take the time to read through the [PDF Manual](https://github.com/tomvandeneede/p2pp/blob/dev/docs/P2PP%20user%20manual.pdf) that comes with the distrubution:

If you ave any questions, please address them to the **P2PP Community Help** group on Facebook

## Acknowledgements

Thanks to.....
Tim Brookman for the co-development of this plugin.
Klaus, Khalil ,Casey, Jermaul, Paul, Gideon,   (and all others) for the endless testing and valuable feedback and the ongoing P2PP support to the community...it's them driving the improvements...
Kurt for making the instructional video n setting up and using p2pp.

## Make a donation...

If you like this software and want to support its development you can make a small donation to support further development of P2PP.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=t.vandeneede@pandora.be&lc=EU&item_name=Donation+to+P2PP+Developer&no_note=0&cn=&currency_code=EUR&bn=PP-DonationsBF:btn_donateCC_LG.gif:NonHosted)



## **Good luck & happy printing !!!**





