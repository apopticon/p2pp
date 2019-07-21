
__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPL'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'


#########################################
# Variable default values
#########################################
# holds state as to if the gcode was generated by S3D and therefore, do other things. **EXPERIMENTAL**
simplify3d_print = False  # type: bool

# Filament Transition Table
palette_inputs_used = [False,
                       False,
                       False,
                       False]

filament_type = ["",
                 "",
                 "",
                 ""]

filament_description = ["Unnamed",
                        "Unnamed",
                        "Unnamed",
                        "Unnamed"]
filament_color_code = ["-",
                       "-",
                       "-",
                       "-"]


filament_short = [0, 0, 0, 0]

skippable_layer = []

used_filament_types = []

default_splice_algorithm = "D000 D000 D000"
process_warnings = []
splice_algorithm_table = []
splice_algorithm_dictionary = {}

max_tower_z_delta = 0.0
cur_tower_z_delta = 0.0
layer_height = 0.2
layer_count = -1
towerskipped = False

printer_profile_string = ''
default_printerprofile = '50325050494e464f'  # A unique ID linked to a printer configuration profile in the Palette 2 hardware.

input_gcode = []
processed_gcode = []  # final output array with Gcode

# These variables are used to build the splice information table (Omega-30 commands in GCode) that drives the Palette2.
# spliceoffset allows for a correction of the position at which the transition occurs.
# When the first transition is scheduled to occur at 120mm in GCode, you can add a number of mm to push the transition
# further in the purge tower.  This serves a similar function as the transition offset in chroma.
splice_offset = 0  # type: int
splice_extruder_position = []
splice_used_tool = []
splice_length = []

# SIDE WIPES
side_wipe_loc = ""  # type: str
side_wipe = False  # type: bool
side_wipe_length = 0  # type: float
side_wipe_skip = False  # type: bool
define_tower = False  # type: bool
sidewipe_miny = 25  # type: float
sidewipe_maxy = 175  # type: float
max_wipe = -1
wipe_feedrate = 2000  # type: int
empty_grid = False  # type: bool

before_sidewipe_gcode = []
after_sidewipe_gcode = []

filename = ""

bed_size_x = 250  # type: int
bed_size_y = 220  # type: int
bed_origin_x = 0  # type: int
bed_origin_y = -10.00   # type: int  # Account for the purge line at the start of the print

wipe_tower_info = {'minx': 9999,
                   'miny': 9999,
                   'maxx': -9999,
                   'maxy': -9999
                   }

wipetower_posx = 0.0  # type: float
wipetower_posy = 0.0  # type: float

currentPositionX = 0.0  # type: float
currentPositionY = 0.0  # type: float
currentPositionZ = 0.0  # type: float

# ping_extruder_position: Stores information about the PINGS generated by P2PP. This information is pasted after
# the splice information directly below the Palette2 header in GCODE.
ping_extruder_position = []


# hotswapcount: The number of hot-swaps generated during the print. This feature is currently unused.
hotswap_count = 0  # type: int

# TotalExtrusion keeps track of the total extrusion in mm for the print taking into account the Extruder Multiplier set
# in the GCode settings...
total_material_extruded = 0  # type: float

# The next 3 variables are used to generate pings.   A ping is scheduled every ping interval.  The LastPing option
# keeps the last extruder position where a  ping was generated.  It is set to -100 to ping the first PING forward...
# Not sure this is a good idea.   Ping distance increases over the print in an exponential way.   Each ping is 1.03 times
# further from the previous one.   Pings occur in random places!!! as the are non-intrusive and don't causes pauses in the
# print they aren ot restricted to the wipe tower and they will occur as soon as the interval length for ping is exceeded.
last_ping_extruder_position = 0
ping_interval = 350  # type: float
max_ping_interval = 3000  # type: float
ping_length_multiplier = 1.03  # type: float
sidewipe_correction = 1.0  # type: float
sidewipe_retract = 0.4  # type: float
correct_wipe_retract = False  # type: bool
wipe_retracted = False  # type: bool
mmu_unload_remove = False  # type: bool
volumetric_e = False  # type: bool

isReprap_Mode = False  # type: bool

# currenttool/lastLocation are variables required to generate O30 splice info.   splice info is generated at the end of the tool path
# and not at the start hence the requirement to keep the toolhead and lastlocation to perform the magic
current_tool = -1  # type: int
previous_toolchange_location = 0  # type: float

current_layer = "0"    # type: str # Capture layer information for short splice texts
extrusion_multiplier = 1.0  # type: float  # Monitors M221 commands during the print.
extrusion_multiplier_correction = 1.0
current_print_feedrate = 100  # type: int  # Monitors the current feedrate
current_print_feed = 2000  # type: int
extra_runout_filament = 150  # type: int  # Provide extra filament at the end of the print.
min_splice_length = 80  # type: int  # Minimum overall splice length.
min_start_splice_length = 100  # type: int  # Minimum first splice length.
within_tool_change_block = False  # type: bool  # State of processed G-Code to determine if part of a toolchange.
allow_filament_information_update = False  # type: bool  # TBA

reprap_compatible = False  # Enables the cleanup/removal of M900 commands as RepRap uses M572 which is slightly different

gui = True  # Enabled/Disabled by --gui switch - enables GUI Mode which requires tkinter.
consolewait = False

version = "0.0.0"
