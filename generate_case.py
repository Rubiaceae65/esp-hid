from solid import *
from solid.utils import *
from solid.solidpython import scad_render

# Case parameters
CASE_LENGTH = 150  # Overall length of the case
CASE_WIDTH = 100   # Overall width of the case
CASE_HEIGHT = 30   # Overall height of the case
WALL_THICKNESS = 2 # Thickness of the case walls

# Board dimensions (LOLIN S3 Mini)
BOARD_LENGTH = 34.3
BOARD_WIDTH = 25.4
BOARD_THICKNESS = 3 # Approximate thickness of the PCB

# Footswitch parameters
FOOTSWITCH_MOUNT_DIAMETER = 12 # Diameter of the hole for mounting the footswitch
FOOTSWITCH_CAP_DIAMETER = 16   # Diameter of the footswitch cap (for spacing)
FOOTSWITCH_DEPTH = 20          # Depth required for the footswitch inside the case

# Button parameters (for the 7 buttons)
BUTTON_HOLE_DIAMETER = 6 # Diameter of the hole for the small buttons
BUTTON_SPACING = 15      # Spacing between small buttons

# USB-C port dimensions (approximate)
USB_C_WIDTH = 10
USB_C_HEIGHT = 5
USB_C_DEPTH = 7

# LED hole diameter
LED_HOLE_DIAMETER = 3

# Standoff parameters for board mounting
BOARD_STANDOFF_DIAMETER = 4
BOARD_STANDOFF_HEIGHT = 5
BOARD_STANDOFF_SCREW_DIAMETER = 2.5

# Lid assembly parameters
LID_OVERLAP = 5 # How much the lid walls overlap the base walls
SCREW_DIAMETER = 3 # For M3 screws
SCREW_HEAD_DIAMETER = 6 # For countersunk or pan head screws
SCREW_HOLE_DEPTH = 5 # Depth of screw hole in base
LID_SCREW_STANDOFF_HEIGHT = 5 # Height of standoffs for lid screws in the base

def create_base_part():
    # Base plate
    base_plate = cube([CASE_LENGTH, CASE_WIDTH, WALL_THICKNESS])

    # Lower walls
    lower_wall_height = CASE_HEIGHT / 2 - WALL_THICKNESS / 2 # Half height for base walls
    outer_lower_walls = cube([CASE_LENGTH, CASE_WIDTH, lower_wall_height])
    inner_lower_walls = cube([CASE_LENGTH - 2 * WALL_THICKNESS, CASE_WIDTH - 2 * WALL_THICKNESS, lower_wall_height])
    lower_walls = outer_lower_walls - translate([WALL_THICKNESS, WALL_THICKNESS, 0])(inner_lower_walls)

    # USB cutout
    usb_cutout = translate([
        CASE_LENGTH / 2,
        0, # On the edge
        WALL_THICKNESS + (lower_wall_height - USB_C_HEIGHT) / 2 # Centered vertically in lower wall
    ])(cube([USB_C_WIDTH, WALL_THICKNESS + 0.1, USB_C_HEIGHT], center=True))

    # Board standoffs
    board_standoffs = []
    board_screw_holes = []
    offset_from_edge = 5 # Distance from board edge to mounting hole center
    standoff_positions = [
        [ (CASE_LENGTH / 2) - (BOARD_LENGTH / 2) + offset_from_edge,
          (CASE_WIDTH / 2) - (BOARD_WIDTH / 2) + offset_from_edge,
          WALL_THICKNESS ],
        [ (CASE_LENGTH / 2) + (BOARD_LENGTH / 2) - offset_from_edge,
          (CASE_WIDTH / 2) - (BOARD_WIDTH / 2) + offset_from_edge,
          WALL_THICKNESS ],
        [ (CASE_LENGTH / 2) - (BOARD_LENGTH / 2) + offset_from_edge,
          (CASE_WIDTH / 2) + (BOARD_WIDTH / 2) - offset_from_edge,
          WALL_THICKNESS ],
        [ (CASE_LENGTH / 2) + (BOARD_LENGTH / 2) - offset_from_edge,
          (CASE_WIDTH / 2) + (BOARD_WIDTH / 2) - offset_from_edge,
          WALL_THICKNESS ]
    ]
    for pos in standoff_positions:
        x, y, z = pos[0], pos[1], pos[2]
        board_standoffs.append(translate([x, y, z])(cylinder(d=BOARD_STANDOFF_DIAMETER, h=BOARD_STANDOFF_HEIGHT)))
        board_screw_holes.append(translate([x, y, z])(cylinder(d=BOARD_STANDOFF_SCREW_DIAMETER, h=BOARD_STANDOFF_HEIGHT + 0.1)))

    # Lid screw holes (blind holes in the base)
    lid_screw_positions = [
        [WALL_THICKNESS + 5, WALL_THICKNESS + 5, WALL_THICKNESS + LID_SCREW_STANDOFF_HEIGHT],
        [CASE_LENGTH - WALL_THICKNESS - 5, WALL_THICKNESS + 5, WALL_THICKNESS + LID_SCREW_STANDOFF_HEIGHT],
        [WALL_THICKNESS + 5, CASE_WIDTH - WALL_THICKNESS - 5, WALL_THICKNESS + LID_SCREW_STANDOFF_HEIGHT],
        [CASE_LENGTH - WALL_THICKNESS - 5, CASE_WIDTH - WALL_THICKNESS - 5, WALL_THICKNESS + LID_SCREW_STANDOFF_HEIGHT]
    ]
    lid_screw_holes = []
    lid_screw_standoffs = []
    for pos in lid_screw_positions:
        x, y, z = pos[0], pos[1], pos[2]
        lid_screw_standoffs.append(translate([x, y, WALL_THICKNESS])(cylinder(d=SCREW_HEAD_DIAMETER, h=LID_SCREW_STANDOFF_HEIGHT)))
        lid_screw_holes.append(translate([x, y, WALL_THICKNESS])(cylinder(d=SCREW_DIAMETER, h=LID_SCREW_STANDOFF_HEIGHT + SCREW_HOLE_DEPTH)))

    base_part = union()(base_plate, lower_walls) - usb_cutout
    base_part += union()(board_standoffs) - union()(board_screw_holes)
    base_part += union()(lid_screw_standoffs) - union()(lid_screw_holes)

    return base_part

def create_lid_part():
    # Top plate
    top_plate = cube([CASE_LENGTH, CASE_WIDTH, WALL_THICKNESS])

    # Upper walls (overlap the base walls)
    upper_wall_height = CASE_HEIGHT / 2 + WALL_THICKNESS / 2
    outer_upper_walls = cube([CASE_LENGTH, CASE_WIDTH, upper_wall_height])
    inner_upper_walls = cube([CASE_LENGTH - 2 * WALL_THICKNESS, CASE_WIDTH - 2 * WALL_THICKNESS, upper_wall_height])
    upper_walls = outer_upper_walls - translate([WALL_THICKNESS, WALL_THICKNESS, 0])(inner_upper_walls)

    # Footswitch holes
    total_footswitch_width = 7 * FOOTSWITCH_CAP_DIAMETER + 6 * BUTTON_SPACING
    start_x = (CASE_LENGTH - total_footswitch_width) / 2 + FOOTSWITCH_CAP_DIAMETER / 2
    footswitch_holes = []
    for i in range(7):
        hole_pos_x = start_x + i * (FOOTSWITCH_CAP_DIAMETER + BUTTON_SPACING)
        footswitch_holes.append(translate([hole_pos_x, CASE_WIDTH / 2, WALL_THICKNESS])(cylinder(d=FOOTSWITCH_MOUNT_DIAMETER, h=WALL_THICKNESS + FOOTSWITCH_DEPTH + 0.1)))

    # LED hole
    led_hole = translate([
        CASE_LENGTH / 2 - USB_C_WIDTH / 2 - 5, # Offset from USB port
        WALL_THICKNESS / 2, # On the edge
        WALL_THICKNESS # On the top surface
    ])(cylinder(d=LED_HOLE_DIAMETER, h=WALL_THICKNESS + 0.1, center=True))

    # Lid screw through-holes
    lid_screw_positions = [
        [WALL_THICKNESS + 5, WALL_THICKNESS + 5, 0],
        [CASE_LENGTH - WALL_THICKNESS - 5, WALL_THICKNESS + 5, 0],
        [WALL_THICKNESS + 5, CASE_WIDTH - WALL_THICKNESS - 5, 0],
        [CASE_LENGTH - WALL_THICKNESS - 5, CASE_WIDTH - WALL_THICKNESS - 5, 0]
    ]
    lid_screw_through_holes = []
    for pos in lid_screw_positions:
        x, y, z = pos[0], pos[1], pos[2]
        lid_screw_through_holes.append(translate([x, y, z])(cylinder(d=SCREW_DIAMETER + 0.5, h=WALL_THICKNESS + 0.1)))

    lid_part = union()(top_plate, upper_walls) - union()(footswitch_holes) - led_hole - union()(lid_screw_through_holes)

    return lid_part

if __name__ == '__main__':
    # Generate Base Part
    file_out_base = open("esp32_footswitch_case_base.scad", "w")
    file_out_base.write(scad_render(create_base_part()))
    file_out_base.close()
    print("Generated esp32_footswitch_case_base.scad")

    # Generate Lid Part
    file_out_lid = open("esp32_footswitch_case_lid.scad", "w")
    file_out_lid.write(scad_render(create_lid_part()))
    file_out_lid.close()
    print("Generated esp32_footswitch_case_lid.scad")