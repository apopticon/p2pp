# p2pp - **Palette2 Post Processing tool for Slic3r PE**


**Tested with version 1.41.2 and 1.42.0 Beta 1**
earlier versions may generate different code patterns and may not work correctly


## Changelog

-  21/05/2019 - Code refqctor - no functionality change
-  31/05/2019 - Added -w [0|1] parameter to enable/disable the waiting for user feedback after rgenerating the report.
-  06/06/2019 - Added correction for gcode patchup synchronization when generatin code in REPRAP mode
-  06/06/2019 - Added check on the correctness of the printer profile sting (lenght/allowed characters)
-  06/06/2019 - Added default printer profile 50325050494e464f is no user defined one exists
-  25/06/2019 - Corrected for allowance of fractional linear advance values
-  30/06/2019 - Added PROFILETYPEOVERRIDE parameter
-  30/06/2019 - Corrected traveling speed issue to side wipe
-  30/06/2019 - BETA - added asynchonous tower function


## Purpose

Allow Palette 2 users to exploit all features and functionality of the palette 2 (Pro) with the Slic3r PE functionality for multi material printing including:

- use of variable layers without bloating the wipe tower
- wipe to waste object
- wipe to infill
- configurable option to create more filament at the end of the print 
- configurable tower print speeds


**IMPORTANT:**
> P2pp currently only works for devices in a connected setup.
> **It does not generate the required sequences to meet the Pause-based pings in accessory mode.**

## Functionality

p2pp is a python script with a shell script/batch file wrapper.

It works as a post processor to GCode files generated by Splic3r PE, just like Chroma does.   If does however not create any new code for wipe towers etc, it just adds Palette 2 MCF information codes to the file.  The script is triggered automatically when exporting GCode or when sending information to the printer so no manual additional step is required.  

**IMPORTANT**
> Prior to using the script it is imperative that you setup the printer according to the specifications set by 
Mosaic( this includes full calibration using canvas or Chroma). 
Follow the guide(s) below and create a new Printer profile as there are some 
settings that contradict the Mosiac Guide for slicing with Chroma. In addition, it's important that your printers 
extruder is calibrated and working correctl

If you are new to printing with Splic3r PE, make sure you have the printer dialed in using single filament prints before
adding the complexity of p2pp post scripting.   It will greatly simplify the debugging if you know the print, filament and printer
settings are porperly tuned to work with your 3d Printer hardware.

## General information

P2PP requires a python interpreter to be installed on your computer.  

MAC OSX based computers should have the reauired Python 2.7 compiler installed by default.

Windows users may not have python installed yet.  For compatibility reasonse we recommend to install version 2.7 or 3.7
from  https://www.python.org/downloads/windows/ 
Make sure to keep track where you installed python as you will need this information in further steps.

## USERS OF SLICER 1.42.0 BETA 1 AND ABOVECAN SKIP TO THE CONFIGURATION OF SLIC3R PE

## WINDOWS INSTALLATION 


> When updating p2pp to a new version all configuration in the .bat file is overwritten.  Make sure to put the .bat file aside before replacing the directory content.  Copy the file over the newly unzipped file to complete the installation.


1. Clone this Github repository to a zip file and extract this zipfile to a location of your choice.
2. Download and Install Python. P2PP is currently compatible with both Python 2.7 and 3.7. https://www.python.org/downloads/windows/
3. In the .bat file change the following.
- Change "c:\python27\python.exe" to your python.exe path
- Change "c:\p2pp\p2pp.py" to the the path of p2pp.py (which you downloaded earlier)
``` 
c:\python27\python.exe c:\p2pp\p2pp.py -i %1
``` 




## Unix / Mac OSX INSTALLATION

> When updating p2pp to a new version all configuration in the .bat file is overwritten.  Make sure to put the .bat file aside before replacing the directory content.  Copy the file over the newly unzipped file to complete the installation.

1. Clone this Github repository to a zip file and extract this zipfile to a location of your choice. 
2. You will need either python 2.7 or python 3 to be installed on your machine.
3. Further when running on a unix-flavoured system (Mac OSX or Linux), you will need to make the script p2pp.sh executable:
```
cd place_where_you_extracted_the_zip_file
chmod 755 p2pp.sh
chmod 755 P2PP.py
```

Test your work by typing `./p2pp.sh` and it should bring up a message windows 
telling you it could not find the input file

This indicates all files are properly setup and has executed correctly.
The remainder of the configuration is done in **Slic3r PE**

## Configuration of Slic3r PE:
**NOTE:**
> For now, there is no error checking on some of the P2PP codes. You need to ensure that they are followed **exactly**. **They are CaSe SeNSiTiVE!**

If you want a head-start, you can import the configuration file in the splic3r_templates subfolder.  This file contains PLA Filament, print and printer definitions.   

**MANDATORY STEPS:**
1. Open one of the .mcf.gcode you recently sliced with Canvas or Chroma. It's important that you use a file that has been 
printed and or previously calibrated with to save manual additional steps. A mistake here will trigger recalibration with 
your printer for a new printer profile.
2. Near the top of the gcode there should be a line starting with "O22 Dxxxxxxxxxxxxxxxxxxxx".
3. Copy _everything_ **_after_** the "D". This is your Printer Profile ID. Note this down and have it ready for the next steps. (Copy and paste, don't type it).
E.G. If your O22 line reads "O22 De827315ff39aaaaa", then your printer profile is: e827315ff39aaaaa  
4. Make sure the bed origin and bed siwe are defined correctly. p2pp will remove all extrusion outside of the bed.  Leaving the default values (for Prusa MK3) might result in failed prints.

### Printer Settings
1. In Slic3r, Click the "Printer Settings Tab".
2. Click the "Custom G-code" menu item.
3. Locate the "Start G-code" input box at the top.
4. INSERT (not overwrite) the following lines at the TOP of the Start G-code. You'll note that they are all commented out and are in no way going to interfere with the print.
5. all movements outside the defined bedsize WILL be commented out.   If you do a pruge line outside of the bed area make sure to include this part of the bed in the bed definition

    ```
    ;P2PP PRINTERPROFILE=REPLACE_WITH_YOUR_PRINTER_PROFILE_OBTAINED_FROM_ABOVE
    ;P2PP SPLICEOFFSET=30
    ;P2PP MINSTARTSPLICE=100
    ;P2PP MINSPLICE=80
    ;P2PP MATERIAL_DEFAULT_0_0_0
    ;P2PP MATERIAL_PVA_PVA_0_0_0
    ;P2PP MATERIAL_PVA_PLA_0_0_0
    ;P2PP MATERIAL_PLA_PLA_0_0_0
    ;P2PP MATERIAL_PET_PET_0_0_0
    ; even is you are not using SIDE TRANSITIONS, make sure the bed is defined correctly!!
    ; the default settings will match Pruse MK3(s) printers.
    ;P2PP BEDORIGINX=0
    ;P2PP BEDORIGINY=-10
    ;P2PP BEDSIZEX=250
    ;P2PP BEDSIZEY=220
    ;P2PP  PURGETOWERDELTA=0
        
    ; Following settings are optional (see description below)
    
    ;P2PP LINEARPING
    ;P2PP EXTRAENDFILAMENT=150
    
    ; Following optional settings control the SIDE TRANSITIONING (see description below)

    ;P2PP SIDEWIPELOC=X253.9
    ;P2PP SIDEWIPEMINY=45
    ;P2PP SIDEWIPEMAXY=195
    ;P2PP SIDEWIPECORRECTION=1.0
    ;P2PP BEFORESIDEWIPEGCODE ;--ENTER GCODE TO BE EXECUTED BEFORE SIDEWIPE (one coomand per line,can be multiple lines)
    ;P2PP AFTERSIDEWIPEGCODE ;--- ENTER GCODE TO BE EXECUTED AFTER SIDEWIPE (one coomand per line,can be multiple lines)
    
    ```

 ![splice offset](https://github.com/tomvandeneede/p2pp/blob/dev/docs/overallconfig.png)



5. In the "After layer change G-code" INSERT (not overwrite) the following line.
    ```
    ;LAYER [layer_num]
    ```
6. Click the "General" menu item.
7. Locate "Capabilities".
8. Change Extruders to "4".
9. **ENABLE** "Single Extruder Multi Material" (Contradicts Mosaic Instructions).
10. Click "Single Extruder MM Setup" menu item.
11. Change ALL entries within "Single Extruder MM Setup" to 0.
12. Click Each of the Extruders (1,2,3 & 4) and ensure their settings are Identical to each other (except the extruder colour)
13. Click the floppy-disk icon, and append "Palette P2PP" to the end of the Printer Settings profile name.

> **SPLICEOFFSET** 
    Is the amount of mm added to the first splice.  It works in a similar way to the transition position % from Chroma and Canvas.  Here the value is a fixed length.  In our testing, 30mm seemed to be a good position resulting in perfect prints. You may want to tweak this value if you find the transition happens too early or too late.
   ```
  ;P2PP SPLICEOFFSET=30
  ``` 
  
  ![splice offset](https://github.com/tomvandeneede/p2pp/blob/dev/docs/spliceoffset.png)
  
  
> **MATERIAL_XXX_XXX\_#\_#\_#**
    This is used to to define heat/compression/cooling settings for the splice between materials. The MATERIAL_DEFAULT setting provides a configurable fallback in case no profile is defined for the material combination. Please be aware that entries are not symmetrical and you need to define the settings for both directions in order to specify a complete process. The definition is as per standard Chroma and Canvas profiles. Order of parameters is CURRENT-MATERIAL/NEW-MATERIAL/HEAT/COMPRESSION/COOLING. Default is all 0 as per standard in Chroma and Canvas.
   ```
  ;P2PP MATERIAL_PLA_PLA_0_0_0
  ``` 

> **LINEARPING**  *[OPTIONAL]*
    This is used to keep the filament disctance between pings constant to 350mm.  When this parameter is not set, the ping distance is exponentially growing during the print resulting in filament distances up to 3m between pings in very long prints.  ** WARNING ** Smoe users have reported issues when setting LINEARPING to values below 350mm.  It is suggested to keep 350 as a minimum.
   ```
  ;P2PP LINEARPING=350
  ```    
  ![splice offset](https://github.com/tomvandeneede/p2pp/blob/dev/docs/linearping.png)
    
> **EXTRAENDFILAMENT=\#** *[OPTIONAL]*
  This parameter is used to configure the extra length (in mm) of filament P2 will generate at the end of the print.  The default parameter value is defined as 150mm.  The value should at least be the length between the extruder motor to the nozzle. 
  
   ```
  ;P2PP EXTRAENDFILAMENT=150
  ```
 
  > **BEDORIGINX=nnn  and BEDORIGINY=nnn#** 
   Sets the origin of the bed.  The default value is as defined below and should suite MK3 users.  Users of other printers can override the defaults by using the below lines with the correct values in the printer Startup GCode sectio.   These parameters are used to determine if the purge tower is located on the bed or not.
   
   ```
  ;P2PP BEDORIGINX=0.0
  ;P2PP BEDORIGINY=-1.0
  ```
  
  > **BEDSIZEX=nnn  and BEDSIZEY=nnn#** 
  Sets the size of the bed.  The default value is as defined below and should suite MK3 users.  Users of other printers can override the defaults by using the below lines with the correct values in the printer Startup GCode section.   These parameters are used to determine if the purge tower is located on the bed or not.
      
   ```
  ;P2PP BEDSIZEX=250
  ;P2PP BEDSIZEY=220
  ```

 > **;P2PP WIPEFEEDRATE=nnnn** *[EXPERIMENTAL,OPTIONAL]*
   Sets the print speed when purging filament.  This parameter is defined in **mm/min**.  If not defined the print speed set by Slic3r is used.
   ``` 
  ;P2PP WIPEFEEDRATE=2400
  ;sets the print speed to 40mm/s
  ```  
   
 > **  ;P2PP PURGETOWERDELTA=0** *[EXPERIMENTAL,OPTIONAL]*
 
 The PURGETOWERDELTA feature allows the purge tower to grow less quickly than the 
 actual print up to a certain amount.  P2PP will remove empty grid layers from the tower
 until the maximum height difference is reached.  This reduces filament consumption as well as time spent in the purge tower
 
 It is important to assure the extruder assembly will NOT hit the already printed parts on the bed.
 Also when the difference becomes too big the time to drop and rise will start to have an impact on the print time.
 
The default value is 0 - meaning the feature is not enabled.

  ``` 
   ;P2PP PURGETOWERDELTA=10
  ;allows the purge tower to be 10mm lower than the actual print
  ```  
 
 > **SIDEWIPELOC=X#** *[EXPERIMENTAL,OPTIONAL]*
  This is used to define the location on the X-Axis the printer needs to go to to do a side transition instead of doing a tower purge.  In Slic3r all still needs to be setup with a purge, tower, but the tower needs to be **MOVE COMPLETELY OFF THE BED** to enable the SIDE WIPE .  p2pp will convert the tower purges into side wipes and fileter out all purges that are not necessary (i.e. empty towe shells). 
  If you want to perform a side wipe on the MK3 use the following line.  
  ```
  ;P2PP SIDEWIPELOC=X254
  ```

 > **WIPEFEEDRATE=nnnn** *[OPTIONAL]*
  This parameter is used to define the feedrate at which purging moved happens.  The default value is 2000mm/min but an override can be set through this parameter.  The value entered is in mm/min.
  ```
  ;P2PP SIDEWIPELOC=2000
  ```

> **SIDEWIPEMINY=nnnn** and **SIDEWIPEMAXY=nnnn**
  These values allow control over the Y movement during the wipe.  Default values are 45 for the minimal value, 195 for the maximal value.  The user can extend/restrict these values if needed.  Setting these parameters does not affect the speed at which the extrusion takes place. 
  ```
  ;P2PP SIDEWIPMINY=45
  ;P2PP SIDEWIPEMAXY=195
  ```
  
> **SIDEWIPECORRECTION=** *[OPTIONAL]*
  This parameter is introduced to correct for inconsistent extrusion that may occur when doing side transitions.  If you notice that during the side transition, the printer over or underextrudes for some reason, you can enter a value here between 0.9 and 1.1 that acts as a local extrusion multiplier DURING the extrusion.  Default value is 1.0
  ```
  ;P2PP SIDEWIPECORRECTION=1.0
  ```

> **;P2PP BEFORESIDEWIPEGCODE** and **;P2PP AFTERSIDEWIPEGCODE** *[OPTIONAL]*
  These parameters allow the user to insert blocks of GCode right before or after the side wipe purge block is executed.  There can be only one GCode command per line but you can include multiple BEFORE/AFTERSIDEWIPEGCODE commands in the section.  The commands are always executed in the given order.



> **;P2PP REPRAPCOMPATIBLE**  *[OPTIONAL]*
  Enhances the compatibility with RepRap type boards (e.g. Duet) by filtering out Slic3r default commands that are incompatible with this firmware

### Print Settings
1. In Slic3r, Click the "Print Settings Tab"
2. Click the "Multiple Extruders" menu item
3. Locate "Wipe tower"
4. Ensure "Wipe tower" **IS ENABLED** (Contradicts Mosaic Instructions)
5. Ensure "Prime all printing extruders" is **DISABLED**
6. Click the "Output Options" menu item
7. Locate the "Post-processing scripts" input box at the bottom


**when you are using Slic3r PE version 1.42.0 Alpha or before:**

 Put the full name of the .sh (unix/Mac OSX) or .bat (Windows) in this input box.  Include the full path (don't use ~ for OSX).  Add no parameters.
```
    For Windows: c:\yourpath\p2pp.bat
    For Mac/Unix: /yourpath/p2pp.sh
```

Click the floppy-disk icon, and append "Palette P2PP" to the end of the Print Settings profile name.
    
**when you are using Slic3r PE version 1.42.0 BETA or later:**    

For Windows: 
   
```
    c:\your_python_path\python.exe your_p2pp_path\P2PP.py -i
```
    
For Mac/Unix: 

```
    python your_p2pp_path/p2pp/P2PP.py -i ;
```    
  
  
    
    
Click the floppy-disk icon, and append "Palette P2PP" to the end of the Print Settings profile name.

**NOTE:**
> The minimal first slice length is 100mm. This is required to make the filament reach the outgoing drive. Minimum slice distance for following slices can be set as low as 40, however this will impact the speed at which filament can be created and so print speed may have to be adjusted accordingly


### Filament Settings (!!!)
1. In Slic3r, Click the "Filament Settings Tab"
2. Each filament should define a linear advance factor of greater than 0 (nn value).  
Normally filament has this value defined based on bowden or direct drive so no action is required.
```
M900 Knn
```

 Remember to click the floppy-disk icon to save!

 > **PROFILETYPEOVERRIDE=** *[OPTIONAL]*
 
In case you are using different brands of the same type of material that require different splicing profile settings, PROFILETYPEOVERRIDE is defined in the filament start g-code as follows:

```
;P2PP PROFILETYPEOVERRIDE=PLA2
```

Doing this will allow you to specify the splice characteristics between regular PLA and the new filament type PLA2 as for other materials.
This feature is intended for use with different brands of the same material that would otherwise not splice together properly

```
;P2PP MATERIAL_PLA2_PLA_a_b_c
;P2PP MATERIAL_PLA_PLA2_d_e_f
```

## Usage

When setup correctly the script will be triggered automatically from Slic3r PE and exported files will contain the mcf header required for palette operation. This functionality will only be enabled when selecting the right print/filament and printer profiles so when selecting any other profiles, single filament file generation will happen as before.

During the conversion the script may come up with a window stating possible warninngs.

The purge settings in Slic3r PE are defined under the purge volumes settings.  This button is only visible on the "Plater Tab" and only when a Multi-Material Printer Profile is selected when "Multi Material, Single Extruder" is enabled.  The information entered in this screen is volumetric. This means that you have to roughly multiply the number in these fields by a factor 2.4 in order to get the filament length. We've found that 180mm3 (75mm of Filament) works well.
![purging volumes](https://github.com/tomvandeneede/p2pp/blob/master/docs/Unloading_settings.JPG)
> You do not need to set any volume for "Unloaded" - Leave this as 0. 


> SLIC3R PE uses volume instead of length in the purge settings.  For 1.75mm filament, 1mm of filament repesents a volume of approx 2.4mm3.  In order to relate to values used in Chroma or Canvas,you have to divide the Slic3r PE values by a factor 2.4!
   


On your first prints make sure you review the output file to make sure it contains the Omega header. (bunch of commands starting with capital letter O (oh))

**If slices are too short:**
> Increase the purge volumes until the required length is met (or lower the P2PP_MINSPLICE setting). If the start slice is too short, you can add a brim or skirt to use more filament in the first color.


## Extrusion Multipliers with P2PP

Extrusion multipliers increase or decrease the effective extrusion by a factor defined in the **M221** Gcode command.  Prusa MK3 users may know the following piece of text appearing in their startup Gcode:

```
	M221 S{if layer_height==0.05}100{else}95{endif}
```

This piece of code sets a specific extruder mulpiplier depending on the chosen layer height.

So….  What does this mean in real life?

When you issue **M221 M95** (standard on a Prusa, 0.20mm layer),  you will tell the printer to use only 95% of the material specified in the Gcode file.    **G1 E100**  - the command to extrude 100mm of filament - will make the printer consume *only 95mm* of filament… 

In this examply, when you calibrate yur P2 or P2Pro using an extrusion multiplier, P2/P2Pro will assume your printer  is underconsuming filament. On a standard Prusa MK3 with a keychain sliced using SLic3R PE it would not be uncommon to see PINGS in range of 95%.

For good measure, it is therefor important to make sure your extrusion multiplier is set to 100% during the first calibration print.  You can achieve this by (temporarely) adding the following line at the end of your startup GCODE:

```
	M221 S100
```

For all future prints using **Chroma** or **Canvas**, make sure to keep the same line in the code!  Removing the line will potentially generate a gap that P2/P2P will not be able to correct for.... 

**P2PP** however takes the extrusion multiplier into consideration when calculating splice lengths and the ping locations, so even when the printer was calibrated with a value of 100, it will happily print with any other extrusion multiplier (like the 95 on prusa).  Important though to also here use 100% extrusion during the Calibration.

**One big exception:**  Extrusion multiplication settings in *Octoprint* or on the *Printer control panel* should be left at 100% AT ALL TIMES.   P2 and the printer have  filament lengths defined during the GCode-processing.  After the GCode is generated, all actions that affect the amount of filament used will make the printer wander off from its set path.... P2 will try to correct for the error and it may succeed but it puts yout print at risk....


## Acknowledgements

Thanks to Tim Brookman for the co-development of this plugin.

Many thanks also to Klaus, Khalil ,Casey, Jermaul, Paul  (and all others) for the endless testing and valuable feedback and the ongoing P2PP support to the community...it's them driving the improvements...


## **Good luck & happy printing !!!**





