import ezdxf
from config import *

# Case parameters
# All parameters are now imported from config.py

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

def generate_lasercut_case(case_length, case_width, case_height, wall_thickness, material_thickness, num_buttons, footswitch_cap_diameter, button_spacing, footswitch_mount_diameter, led_offset_x, led_offset_y, led_hole_diameter, screw_offset, screw_diameter, board_length, board_width, board_standoff_screw_diameter, usb_c_width, usb_c_height, usb_c_offset_from_bottom):
    # Top Plate
    doc_top = ezdxf.new("R2010")
    msp_top = doc_top.modelspace()
    msp_top.add_lwpolyline([(0,0), (case_length,0), (case_length,case_width), (0,case_width), (0,0)], close=True)

    # Footswitch holes on top plate
    total_footswitch_width = num_buttons * footswitch_cap_diameter + (num_buttons - 1) * button_spacing
    start_x = (case_length - total_footswitch_width) / 2 + footswitch_cap_diameter / 2
    for i in range(num_buttons):
        hole_pos_x = start_x + i * (footswitch_cap_diameter + button_spacing)
        msp_top.add_circle((hole_pos_x, case_width / 2), footswitch_mount_diameter / 2)

    # LED hole on top plate
    msp_top.add_circle((case_length - led_offset_x, case_width - led_offset_y), led_hole_diameter / 2)

    # Screw holes for lid assembly
    screw_positions = [
        (screw_offset, screw_offset),
        (case_length - screw_offset, screw_offset),
        (screw_offset, case_width - screw_offset),
        (case_length - screw_offset, case_width - screw_offset)
    ]
    for x, y in screw_positions:
        msp_top.add_circle((x, y), screw_diameter / 2)

    doc_top.saveas("esp32_lasercut_case_top.dxf")
    print("Generated esp32_lasercut_case_top.dxf")

    # Bottom Plate
    doc_bottom = ezdxf.new("R2010")
    msp_bottom = doc_bottom.modelspace()
    msp_bottom.add_lwpolyline([(0,0), (case_length,0), (case_length,case_width), (0,case_width), (0,0)], close=True)

    # Board mounting holes on bottom plate
    board_offset_from_edge = 5
    board_mounting_hole_positions = [
        ( (case_length / 2) - (board_length / 2) + board_offset_from_edge,
          (case_width / 2) - (board_width / 2) + board_offset_from_edge ),
        ( (case_length / 2) + (board_length / 2) - board_offset_from_edge,
          (case_width / 2) - (board_width / 2) + board_offset_from_edge ),
        ( (case_length / 2) - (board_length / 2) + board_offset_from_edge,
          (case_width / 2) + (board_width / 2) - board_offset_from_edge ),
        ( (case_length / 2) + (board_length / 2) - board_offset_from_edge,
          (case_width / 2) + (board_width / 2) - board_offset_from_edge )
    ]
    for x, y in board_mounting_hole_positions:
        msp_bottom.add_circle((x, y), board_standoff_screw_diameter / 2)

    # Screw holes for lid assembly (matching top plate)
    for x, y in screw_positions:
        msp_bottom.add_circle((x, y), screw_diameter / 2)

    doc_bottom.saveas("esp32_lasercut_case_bottom.dxf")
    print("Generated esp32_lasercut_case_bottom.dxf")

    # Side Panels (Front/Back, Left/Right)
    # Front/Back panels
    doc_front_back = ezdxf.new("R2010")
    msp_front_back = doc_front_back.modelspace()
    msp_front_back.add_lwpolyline([(0,0), (case_length,0), (case_length,case_height), (0,case_height), (0,0)], close=True)
    # USB-C cutout on one of the front/back panels (e.g., front)
    msp_front_back.add_lwpolyline([
        (case_length / 2 - usb_c_width / 2, usb_c_offset_from_bottom),
        (case_length / 2 + usb_c_width / 2, usb_c_offset_from_bottom),
        (case_length / 2 + usb_c_width / 2, usb_c_offset_from_bottom + usb_c_height),
        (case_length / 2 - usb_c_width / 2, usb_c_offset_from_bottom + usb_c_height),
        (case_length / 2 - usb_c_width / 2, usb_c_offset_from_bottom)
    ], close=True)
    doc_front_back.saveas("esp32_lasercut_case_front_back.dxf")
    print("Generated esp32_lasercut_case_front_back.dxf")

    # Left/Right panels
    doc_left_right = ezdxf.new("R2010")
    msp_left_right = doc_left_right.modelspace()
    msp_left_right.add_lwpolyline([(0,0), (case_width,0), (case_width,case_height), (0,case_height), (0,0)], close=True)
    doc_left_right.saveas("esp32_lasercut_case_left_right.dxf")
    print("Generated esp32_lasercut_case_left_right.dxf")

if __name__ == '__main__':
    generate_lasercut_case(
        CASE_LENGTH, CASE_WIDTH, CASE_HEIGHT, WALL_THICKNESS, MATERIAL_THICKNESS,
        NUM_BUTTONS, FOOTSWITCH_CAP_DIAMETER, BUTTON_SPACING, FOOTSWITCH_MOUNT_DIAMETER,
        LED_OFFSET_X, LED_OFFSET_Y, LED_HOLE_DIAMETER, SCREW_OFFSET, SCREW_DIAMETER,
        BOARD_LENGTH, BOARD_WIDTH, BOARD_STANDOFF_SCREW_DIAMETER, USB_C_WIDTH, USB_C_HEIGHT, USB_C_OFFSET_FROM_BOTTOM
    )