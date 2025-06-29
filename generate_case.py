from solid import *
from solid.utils import *
from solid.solidpython import scad_render
from config import *

# Case parameters
# All parameters are now imported from config.py

def create_base():
    # Base of the case
    base = cube([CASE_LENGTH, CASE_WIDTH, WALL_THICKNESS])
    return base

def create_walls():
    # Outer dimensions of the walls
    outer_walls = cube([CASE_LENGTH, CASE_WIDTH, CASE_HEIGHT])
    # Inner dimensions of the walls (creates the hollow space)
    inner_walls = cube([CASE_LENGTH - 2 * WALL_THICKNESS, CASE_WIDTH - 2 * WALL_THICKNESS, CASE_HEIGHT - WALL_THICKNESS])
    # Subtract inner from outer to get just the walls
    walls = outer_walls - translate([WALL_THICKNESS, WALL_THICKNESS, WALL_THICKNESS])(inner_walls)
    return walls

def create_top_lid():
    # Top lid is a thin plate
    lid = cube([CASE_LENGTH, CASE_WIDTH, WALL_THICKNESS])
    return lid

def create_footswitch_holes():
    # Arrange 7 footswitches in a row on the top lid
    # Calculate total width needed for footswitches
    total_footswitch_width = NUM_BUTTONS * FOOTSWITCH_CAP_DIAMETER + (NUM_BUTTONS - 1) * BUTTON_SPACING
    
    # Start position for the first footswitch (centered)
    start_x = (CASE_LENGTH - total_footswitch_width) / 2 + FOOTSWITCH_CAP_DIAMETER / 2
    
    holes = []
    for i in range(NUM_BUTTONS):
        hole_pos_x = start_x + i * (FOOTSWITCH_CAP_DIAMETER + BUTTON_SPACING)
        hole = translate([hole_pos_x, CASE_WIDTH / 2, 0])(cylinder(d=FOOTSWITCH_MOUNT_DIAMETER, h=WALL_THICKNESS + 0.1)) # +0.1 to ensure clean cut
        holes.append(hole)
    return union()(holes)

def create_board_standoffs():
    # Standoffs for the ESP32-S3 board
    # Assuming mounting holes are near the corners of the board
    # Adjust these positions based on actual board mounting holes if known
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

    standoffs = []
    screw_holes = []

    for pos in standoff_positions:
        x, y, z = pos[0], pos[1], pos[2]
        standoffs.append(translate([x, y, z])(cylinder(d=BOARD_STANDOFF_DIAMETER, h=BOARD_STANDOFF_HEIGHT)))
        screw_holes.append(translate([x, y, z])(cylinder(d=BOARD_STANDOFF_SCREW_DIAMETER, h=BOARD_STANDOFF_HEIGHT + 0.1)))

    return union()(standoffs) - union()(screw_holes)

def create_usb_cutout():
    # USB-C port on the side of the case
    # Assuming it's centered on one of the shorter sides
    usb_cutout = translate([
        CASE_LENGTH / 2,
        0, # On the edge
        WALL_THICKNESS + (CASE_HEIGHT - WALL_THICKNESS - USB_C_HEIGHT) / 2 # Centered vertically
    ])(cube([USB_C_WIDTH, WALL_THICKNESS + 0.1, USB_C_HEIGHT], center=True))
    return usb_cutout

def create_led_hole():
    # LED hole on the top surface, near the USB port
    led_hole = translate([
        CASE_LENGTH / 2 - USB_C_WIDTH / 2 - 5, # Offset from USB port
        WALL_THICKNESS / 2, # On the edge
        CASE_HEIGHT - WALL_THICKNESS / 2 # On the top surface
    ])(cylinder(d=LED_HOLE_DIAMETER, h=WALL_THICKNESS + 0.1, center=True))
    return led_hole

def assemble_case():
    base = create_base()
    walls = create_walls()
    top_lid = create_top_lid()
    footswitch_holes = create_footswitch_holes()
    board_standoffs = create_board_standoffs()
    usb_cutout = create_usb_cutout()
    led_hole = create_led_hole()

    # Assemble the main body (base + walls - usb_cutout)
    main_body = union()(base, walls) - usb_cutout

    # Add standoffs to the main body
    main_body = main_body + board_standoffs

    # Assemble the top lid with footswitch holes and LED hole
    # The lid is placed on top of the walls, so its z-position is CASE_HEIGHT - WALL_THICKNESS
    assembled_lid = translate([0, 0, CASE_HEIGHT - WALL_THICKNESS])(top_lid - footswitch_holes - led_hole)

    # Final assembly
    final_case = union()(main_body, assembled_lid)
    return final_case

if __name__ == '__main__':
    file_out = open("esp32_footswitch_case.scad", "w")
    file_out.write(scad_render(assemble_case()))
    file_out.close()
    print("Generated esp32_footswitch_case.scad")
