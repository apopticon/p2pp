__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018-2021, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPLv3'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'

import math
import re

import p2pp.gui as gui
import p2pp.variables as v
import p2pp.p2ppparams as parameters
from p2pp.omega import algorithm_process_material_configuration


def gcode_remove_params(gcode, params):
    removed = False
    result = ''
    rempar = ''
    p = gcode.split(' ')
    for s in p:
        if s == '':
            continue
        if not s[0] in params:
            result += s + ' '
        else:
            rempar = rempar + s + ' '
            removed = True

    result.strip(' ')
    rempar.strip(' ')
    if len(result) < 4:
        return ';--- P2PP Removed [Removed Parms] - ' + gcode

    if removed:
        return result + ";--- P2PP Removed [Removed Parms] - " + rempar
    else:
        return result


def get_gcode_parameter(gcode, parameter, default=None):
    fields = gcode.split()
    for parm in fields:
        if parm[0] == parameter:
            return float(parm[1:])
    return default


def split_csv_strings(s):
    newvalues = []
    keyval = s.split("=")
    if len(keyval) > 1:
        value = ("=".join(keyval[1:])).strip(' ')
        values = value.split(";")
        tmp = None
        idx = 0
        while idx < len(values):
            if tmp is None:
                tmp = values[idx]
            else:
                tmp += values[idx]
            if len(tmp) >= 2:
                if tmp[0] == '"' and tmp[-1] == '"':
                    tmp = tmp[1:-1]
                    res = ""
                    tmp = tmp.replace(" ", "_")
                    for i in list(tmp):
                        if i in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-":
                            res = res + i
                    newvalues.append(res)

                    tmp = ""
            idx += 1
    return newvalues


def filament_volume_to_length(x):
    return x / (v.filament_diameter[v.current_tool] / 2 * v.filament_diameter[v.current_tool] / 2 * math.pi)


def get_bedshape(line):
    bedshape = re.compile("([+-]?\d+(\.\d*)?|\.\d+)")
    coords = bedshape.findall(line)
    if len(coords) >= 8:
        x_coords = []
        y_coords = []

        coords = [float(i[0]) for i in coords]
        for i in range(len(coords)):
            if i % 2:
                y_coords.append(coords[i])
            else:
                x_coords.append(coords[i])

        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)
        v.bed_origin_x = x_min
        v.bed_origin_y = y_min - 5
        v.bed_size_x = x_max - x_min
        v.bed_size_y = y_max - y_min + 5

    if len(coords) != 8:
        v.bed_shape_rect = False

def parse_prusaslicer_config():
    for idx in range(len(v.input_gcode) - 1, -1, -1):

        gcode_line = v.input_gcode[idx]

        if gcode_line.startswith("; estimated printing time"):
            try:
                fields = gcode_line.split(" ")
                if len(fields) == 10 and fields[-4] == "=":
                    v.printing_time = int(fields[-3][:-1])*3600 + int(fields[-2][:-1])*60+int(fields[-1][:-1])
            except (ValueError, IndexError):
                pass
            return

        if gcode_line.startswith("; filament_settings_id"):
            v.filament_ids = split_csv_strings(gcode_line)

        if "generated by PrusaSlicer" in gcode_line:
            try:
                s1 = gcode_line.split("+")
                s2 = s1[0].split(" ")
                v.ps_version = s2[-1]
                gui.create_logitem("File was created with PS version:{}".format(v.ps_version))
                if v.ps_version < "2.2":
                    gui.create_logitem("<b>This version of P2PP is optimized to work with PS2.2 and higher!<b>")
            except [ValueError, IndexError]:
                pass
            continue

        if gcode_line.startswith("; single_extruder_multi_material_priming"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                try:
                    if int(gcode_line[parameter_start + 1:].strip()) == 1:
                        gui.log_warning("[Print Settings][Multiple Extruders][Wipe Tower]Prime all printing extruders MUST be turned off")
                        gui.log_warning("THIS FILE WILL NOT PRINT CORRECTLY")
                except [ValueError, IndexError]:
                    pass
            continue

        if gcode_line.startswith("; wipe_tower_no_sparse_layers"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                try:
                    v.wipe_remove_sparse_layers = (int(gcode_line[parameter_start + 1:].strip()) == 1)
                except [ValueError, IndexError]:
                    pass
            continue

        if gcode_line.startswith("; variable_layer_height"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.variable_layer = int(gcode_line[parameter_start + 1:].strip()) == 1
            continue

        if gcode_line.startswith("; bed_shape") and not v.bed_shape_warning:
            get_bedshape(gcode_line)

        if gcode_line.startswith("; max_print_height"):

            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.z_maxheight = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; wipe_tower_x"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_posx = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; min_skirt_length"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.skirtsize = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; skirts"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.skirts = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; wipe_tower_width"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_width = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; wipe_tower_y"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_posy = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; extrusion_width"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                parm = gcode_line[parameter_start + 1:].strip()
                if parm[-1] == "%":
                    parm = parm.replace("%", "").strip()
                    tmpval = float(parm)
                    v.extrusion_width = v.nozzle_diameter * tmpval / 100.0
                else:
                    v.extrusion_width = float(gcode_line[parameter_start + 1:].strip())

                v.tx_offset = 2 + 4 * v.extrusion_width
                v.yy_offset = 2 + 8 * v.extrusion_width
            continue

        if gcode_line.startswith("; infill_speed"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.infill_speed = float(gcode_line[parameter_start + 1:].strip()) * 60
            continue

        if gcode_line.startswith("; layer_height"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.layer_height = float(gcode_line[parameter_start + 1:].strip())
            continue

        # this next function assumes that the parameters are stored in alphabetical order
        # so layer_height is defined BEFORE first layer height when parsing back to front
        if gcode_line.startswith("; first_layer_height"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                value = gcode_line[parameter_start + 1:].strip()
                if value[-1] == "%":
                    v.first_layer_height = float(value[:-1]) / 100.0 * v.layer_height
                else:
                    v.first_layer_height = float(value)
            continue

        if gcode_line.startswith("; support_material_synchronize_layers"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                tmp = float(gcode_line[parameter_start + 1:].strip())
                v.synced_support = tmp == 1
            continue

        if gcode_line.startswith("; support_material "):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                tmp = float(gcode_line[parameter_start + 1:].strip())
                v.support_material = tmp == 1
            continue

        if gcode_line.startswith("; nozzle_diameter "):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                tmp = gcode_line[parameter_start + 1:].strip().split(",")
                tmp = float(tmp[0])

                v.nozzle_diameter = tmp
            continue

        if gcode_line.startswith("; start_filament_gcode "):
            parameter_start = gcode_line.find("=")
            gcode_value = gcode_line[parameter_start + 2:].strip()
            fields = split_csv_strings(gcode_value)
            for i in range(len(fields)):
                lines = fields[0].split("\\n")
                for line in lines:
                    if line.startswith(";P2PP PROFILETYPEOVERRIDE="):
                        value = line[26:]
                        v.filament_type[i] = value
                        v.used_filament_types.append(v.filament_type[i])
                        v.used_filament_types = list(dict.fromkeys(v.used_filament_types))
            continue

        if gcode_line.startswith("; start_gcode "):
            parameter_start = gcode_line.find("=")
            gcode_value = gcode_line[parameter_start + 2:].strip()
            lines = gcode_value.split("\\n")
            for line in lines:
                m = v.regex_p2pp.match(line)
                if m:
                    if m.group(1).startswith("MATERIAL"):
                        algorithm_process_material_configuration(m.group(1)[9:])
                    else:
                        parameters.check_config_parameters(m.group(1), m.group(2))

        if gcode_line.startswith("; extruder_colour") or gcode_line.startswith("; filament_colour"):
            filament_colour = ''
            parameter_start = gcode_line.find("=")
            gcode_line = gcode_line[parameter_start + 1:].strip()
            parameter_start = gcode_line.find("#")
            if parameter_start != -1:
                filament_colour = gcode_line.split(";")
            v.filament_count = len(filament_colour)
            for i in range(v.filament_count):
                v.filament_color_code[i] = filament_colour[i][1:]

        if gcode_line.startswith("; filament_diameter"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                filament_diameters = gcode_line[parameter_start + 1:].strip(" ").split(",")
                v.filament_diameter = [1.75] * max(len(filament_diameters), 4)
                for i in range(len(filament_diameters)):
                    v.filament_diameter[i] = float(filament_diameters[i])
            continue

        if gcode_line.startswith("; filament_type"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                filament_string = gcode_line[parameter_start + 1:].strip(" ").split(";")
                for i in range(len(filament_string)):
                    if v.filament_type[i] != "":
                        filament_string[i] = v.filament_type[i]
                v.filament_type = filament_string
                v.used_filament_types = list(set(filament_string))
            continue

        if gcode_line.startswith("; retract_lift = "):
            lift_error = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                retracts = gcode_line[parameter_start + 1:].strip(" ").split(",")
                v.retract_lift = [0.6] * max(len(retracts), v.colors)
                for i in range(len(retracts)):
                    v.retract_lift[i] = float(retracts[i])
                    if v.retract_lift[i] == 0:
                        lift_error = True
                        gui.log_warning(
                            "[Printer Settings]->[Extruders 1 -> {}]->[Retraction]->[Lift Z] should not be set to zero.".format(i))
                if lift_error:
                    gui.log_warning("Generated file might not print correctly")
            continue

        if gcode_line.startswith("; retract_length = "):
            retract_error = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                retracts = gcode_line[parameter_start + 1:].strip(" ").split(",")
                v.retract_length = [0.8] * max(len(retracts), v.colors)
                for i in range(len(retracts)):
                    v.retract_length[i] = float(retracts[i])-0.02
                    if v.retract_length[i] < 0.0:
                        retract_error = True
                        gui.log_warning(
                            "[Printer Settings]->[Extruders 1 -> {}]->[Retraction Length] should not be set to zero.".format(i))
                    if retract_error:
                        gui.log_warning("Generated file might not print correctly")
            continue

        if gcode_line.startswith("; gcode_flavor"):
            if "reprap" in gcode_line:
                v.isReprap_Mode = True
            continue

        if "use_firmware_retraction" in gcode_line:
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                gcode_line = gcode_line[parameter_start + 1:].replace(";", "")
                if "1" in gcode_line:
                    gui.log_warning("Hardware retraction no longer supported")
            continue

        if "use_relative_e_distances" in gcode_line:
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                gcode_line = gcode_line[parameter_start + 1:].replace(";", "")
                if not "1" in gcode_line:
                    gui.log_warning("P2PP requires input file with RELATIVE extrusion")
            continue

        if gcode_line.startswith("; wiping_volumes_matrix"):
            wiping_info = []
            _warning = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                wiping_info = gcode_line[parameter_start + 1:].strip(" ").split(",")
                _warning = True
                for i in range(len(wiping_info)):
                    if int(wiping_info[i]) != 140 and int(wiping_info[i]) != 0:
                        _warning = False

                    wiping_info[i] = filament_volume_to_length(float(wiping_info[i]))
            v.max_wipe = max(wiping_info)
            v.wiping_info = wiping_info
            if _warning:
                gui.create_logitem("<b>All purge lengths 70/70 OR 140.  Purge lengths may not have been set correctly.</b>")
            continue
