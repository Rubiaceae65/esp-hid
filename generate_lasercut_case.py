import ezdxf

# Case parameters
CASE_LENGTH = 150  # Overall length of the case
CASE_WIDTH = 100   # Overall width of the case
CASE_HEIGHT = 30   # Overall height of the case
MATERIAL_THICKNESS = 3 # Thickness of the acrylic material
FINGER_JOINT_SIZE = 10 # Size of each finger in the joint

# Board dimensions (LOLIN S3 Mini)
BOARD_LENGTH = 34.3
BOARD_WIDTH = 25.4

# Footswitch parameters
FOOTSWITCH_MOUNT_DIAMETER = 12 # Diameter of the hole for mounting the footswitch
FOOTSWITCH_CAP_DIAMETER = 16   # Diameter of the footswitch cap (for spacing)

# Button parameters (for the 7 buttons)
BUTTON_HOLE_DIAMETER = 6 # Diameter of the hole for the small buttons
BUTTON_SPACING = 15      # Spacing between small buttons

# USB-C port dimensions (approximate)
USB_C_WIDTH = 10
USB_C_HEIGHT = 5
USB_C_OFFSET_FROM_BOTTOM = 5 # Offset from the bottom edge of the side panel

# LED hole diameter
LED_HOLE_DIAMETER = 3
LED_OFFSET_X = 10 # Offset from edge for LED hole
LED_OFFSET_Y = 10 # Offset from edge for LED hole

# Screw hole parameters for assembly
SCREW_DIAMETER = 3.2 # For M3 screws (slightly larger for clearance)
SCREW_OFFSET = 5     # Distance from corner for screw holes

# Standoff parameters for board mounting (holes in bottom plate)
BOARD_STANDOFF_SCREW_DIAMETER = 2.5 # For M2.5 or M3 screws
BOARD_STANDOFF_OFFSET_FROM_EDGE = 5 # Distance from board edge to mounting hole center

def create_finger_joints(length, thickness, joint_size, is_male=True):
    joints = []
    num_joints = int(length / joint_size)
    remaining_length = length - (num_joints * joint_size)
    start_offset = remaining_length / 2

    for i in range(num_joints):
        if (i % 2 == 0 and is_male) or (i % 2 != 0 and not is_male):
            # Male joint (tab)
            joints.append((start_offset + i * joint_size, thickness))
        else:
            # Female joint (slot)
            joints.append((start_offset + i * joint_size, 0))
    return joints

def create_panel(doc, name, width, height, top_joints=None, bottom_joints=None, left_joints=None, right_joints=None):
    msp = doc.modelspace()
    points = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height),
        (0, 0)
    ]
    msp.add_lwpolyline(points, close=True)

    # Add finger joints (simplified for now, just showing concept)
    # Real finger joint generation would be more complex, involving cutting into the main shape
    # This is a placeholder to show where they would be applied.
    if top_joints:
        for x, size in top_joints:
            # Example: msp.add_rect((x, height - size), size, size) # For tabs
            pass
    if bottom_joints:
        for x, size in bottom_joints:
            # Example: msp.add_rect((x, 0), size, size) # For tabs
            pass
    if left_joints:
        for y, size in left_joints:
            # Example: msp.add_rect((-size, y), size, size) # For tabs
            pass
    if right_joints:
        for y, size in right_joints:
            # Example: msp.add_rect((width, y), size, size) # For tabs
            pass

    return msp

def generate_lasercut_case():
    # Top Plate
    doc_top = ezdxf.new("R2010")
    msp_top = doc_top.modelspace()
    msp_top.add_lwpolyline([(0,0), (CASE_LENGTH,0), (CASE_LENGTH,CASE_WIDTH), (0,CASE_WIDTH), (0,0)], close=True)

    # Footswitch holes on top plate
    total_footswitch_width = 7 * FOOTSWITCH_CAP_DIAMETER + 6 * BUTTON_SPACING
    start_x = (CASE_LENGTH - total_footswitch_width) / 2 + FOOTSWITCH_CAP_DIAMETER / 2
    for i in range(7):
        hole_pos_x = start_x + i * (FOOTSWITCH_CAP_DIAMETER + BUTTON_SPACING)
        msp_top.add_circle((hole_pos_x, CASE_WIDTH / 2), FOOTSWITCH_MOUNT_DIAMETER / 2)

    # LED hole on top plate
    msp_top.add_circle((CASE_LENGTH - LED_OFFSET_X, CASE_WIDTH - LED_OFFSET_Y), LED_HOLE_DIAMETER / 2)

    # Screw holes for lid assembly
    screw_positions = [
        (SCREW_OFFSET, SCREW_OFFSET),
        (CASE_LENGTH - SCREW_OFFSET, SCREW_OFFSET),
        (SCREW_OFFSET, CASE_WIDTH - SCREW_OFFSET),
        (CASE_LENGTH - SCREW_OFFSET, CASE_WIDTH - SCREW_OFFSET)
    ]
    for x, y in screw_positions:
        msp_top.add_circle((x, y), SCREW_DIAMETER / 2)

    doc_top.saveas("esp32_lasercut_case_top.dxf")
    print("Generated esp32_lasercut_case_top.dxf")

    # Bottom Plate
    doc_bottom = ezdxf.new("R2010")
    msp_bottom = doc_bottom.modelspace()
    msp_bottom.add_lwpolyline([(0,0), (CASE_LENGTH,0), (CASE_LENGTH,CASE_WIDTH), (0,CASE_WIDTH), (0,0)], close=True)

    # Board mounting holes on bottom plate
    board_offset_from_edge = BOARD_STANDOFF_OFFSET_FROM_EDGE
    board_mounting_hole_positions = [
        ( (CASE_LENGTH / 2) - (BOARD_LENGTH / 2) + board_offset_from_edge,
          (CASE_WIDTH / 2) - (BOARD_WIDTH / 2) + board_offset_from_edge ),
        ( (CASE_LENGTH / 2) + (BOARD_LENGTH / 2) - board_offset_from_edge,
          (CASE_WIDTH / 2) - (BOARD_WIDTH / 2) + board_offset_from_edge ),
        ( (CASE_LENGTH / 2) - (BOARD_LENGTH / 2) + board_offset_from_edge,
          (CASE_WIDTH / 2) + (BOARD_WIDTH / 2) - board_offset_from_edge ),
        ( (CASE_LENGTH / 2) + (BOARD_LENGTH / 2) - board_offset_from_edge,
          (CASE_WIDTH / 2) + (BOARD_WIDTH / 2) - board_offset_from_edge )
    ]
    for x, y in board_mounting_hole_positions:
        msp_bottom.add_circle((x, y), BOARD_STANDOFF_SCREW_DIAMETER / 2)

    # Screw holes for lid assembly (matching top plate)
    for x, y in screw_positions:
        msp_bottom.add_circle((x, y), SCREW_DIAMETER / 2)

    doc_bottom.saveas("esp32_lasercut_case_bottom.dxf")
    print("Generated esp32_lasercut_case_bottom.dxf")

    # Side Panels (Front/Back, Left/Right)
    # Front/Back panels
    doc_front_back = ezdxf.new("R2010")
    msp_front_back = doc_front_back.modelspace()
    msp_front_back.add_lwpolyline([(0,0), (CASE_LENGTH,0), (CASE_LENGTH,CASE_HEIGHT), (0,CASE_HEIGHT), (0,0)], close=True)
    # USB-C cutout on one of the front/back panels (e.g., front)
    msp_front_back.add_lwpolyline([
        (CASE_LENGTH / 2 - USB_C_WIDTH / 2, USB_C_OFFSET_FROM_BOTTOM),
        (CASE_LENGTH / 2 + USB_C_WIDTH / 2, USB_C_OFFSET_FROM_BOTTOM),
        (CASE_LENGTH / 2 + USB_C_WIDTH / 2, USB_C_OFFSET_FROM_BOTTOM + USB_C_HEIGHT),
        (CASE_LENGTH / 2 - USB_C_WIDTH / 2, USB_C_OFFSET_FROM_BOTTOM + USB_C_HEIGHT),
        (CASE_LENGTH / 2 - USB_C_WIDTH / 2, USB_C_OFFSET_FROM_BOTTOM)
    ], close=True)
    doc_front_back.saveas("esp32_lasercut_case_front_back.dxf")
    print("Generated esp32_lasercut_case_front_back.dxf")

    # Left/Right panels
    doc_left_right = ezdxf.new("R2010")
    msp_left_right = doc_left_right.modelspace()
    msp_left_right.add_lwpolyline([(0,0), (CASE_WIDTH,0), (CASE_WIDTH,CASE_HEIGHT), (0,CASE_HEIGHT), (0,0)], close=True)
    doc_left_right.saveas("esp32_lasercut_case_left_right.dxf")
    print("Generated esp32_lasercut_case_left_right.dxf")

if __name__ == '__main__':
    generate_lasercut_case()
