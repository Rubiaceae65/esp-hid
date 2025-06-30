# config.py - Centralized Configuration for ESP32-S3 HID Project

# --- Project-wide Parameters ---
PROJECT_NAME = "ESP32-S3 Dual-Mode HID"

# --- Firmware Parameters (used in src/main.cpp) ---
# Button GPIO assignments (adjust based on your board and wiring)
PIN_ENTER = 4
PIN_ESC = 5
PIN_PAGE_UP = 6
PIN_PAGE_DOWN = 7
PIN_MACRO_1 = 8
PIN_MACRO_2 = 9
PIN_MACRO_3 = 10
PIN_LED = 2 # Common LED_BUILTIN for LOLIN S3 Mini

DEBOUNCE_MS = 50

BLE_KEYBOARD_NAME = "ESP32-S3 Keyboard"
BLE_MOUSE_NAME = "ESP32-S3 Mouse"

# Macro outputs
MACRO_1_OUTPUT = "Macro 1 Output"
MACRO_2_OUTPUT = "Macro 2 Output"
MACRO_3_OUTPUT = "Macro 3 Output"

# --- Case Design Parameters (used in generate_case.py, generate_lasercut_case.py) ---
CASE_LENGTH = 150  # Overall length of the case
CASE_WIDTH = 100   # Overall width of the case
CASE_HEIGHT = 30   # Overall height of the case
WALL_THICKNESS = 2 # Thickness of the case walls (for 3D print)
MATERIAL_THICKNESS = 3 # Thickness of the acrylic material (for laser cut)

BOARD_LENGTH = 34.3 # LOLIN S3 Mini length
BOARD_WIDTH = 25.4  # LOLIN S3 Mini width
BOARD_THICKNESS = 3 # Approximate thickness of the PCB

FOOTSWITCH_MOUNT_DIAMETER = 12 # Diameter of the hole for mounting the footswitch
FOOTSWITCH_CAP_DIAMETER = 16   # Diameter of the footswitch cap (for spacing)
FOOTSWITCH_DEPTH = 20          # Depth required for the footswitch inside the case

BUTTON_HOLE_DIAMETER = 6 # Diameter of the hole for the small buttons
BUTTON_SPACING = 15      # Spacing between small buttons

USB_C_WIDTH = 10
USB_C_HEIGHT = 5
USB_C_DEPTH = 7
USB_C_OFFSET_FROM_BOTTOM = 5 # Offset from the bottom edge of the side panel

LED_HOLE_DIAMETER = 3
LED_OFFSET_X = 10 # Offset from edge for LED hole
LED_OFFSET_Y = 10 # Offset from edge for LED hole

# Standoff parameters for board mounting
BOARD_STANDOFF_DIAMETER = 4
BOARD_STANDOFF_HEIGHT = 5
BOARD_STANDOFF_SCREW_DIAMETER = 2.5

# Lid assembly parameters
LID_OVERLAP = 5 # How much the lid walls overlap the base walls
SCREW_DIAMETER = 3.2 # For M3 screws (slightly larger for clearance)
SCREW_HEAD_DIAMETER = 6 # For countersunk or pan head screws
SCREW_HOLE_DEPTH = 5 # Depth of screw hole in base
LID_SCREW_STANDOFF_HEIGHT = 5 # Height of standoffs for lid screws in the base
SCREW_OFFSET = 5 # Distance from corner for screw holes

# Finger joint parameters for laser cut case
FINGER_JOINT_SIZE = 10 # Size of each finger in the joint

# --- BOM and Estimates Parameters (used in generate_bom_and_estimates.py) ---
FILAMENT_DENSITY_G_MM3 = 1.24e-3 # PLA density (g/mm^3)
FILAMENT_COST_PER_KG = 20 # USD
PRINTING_SPEED_MM3_S = 20 # Very rough average printing speed
INFILL_PERCENTAGE = 0.20 # 20% infill for 3D printed parts

LASER_CUT_SPEED_MM_S = 10 # Very rough average cutting speed
ACRYLIC_COST_PER_MM2 = 0.0001 # Very rough cost per mm^2 for 3mm acrylic

# --- PCB Design Parameters (used in generate_button_pcb.py) ---
NUM_BUTTONS = 7
BUTTON_GPIO_PINS = [4, 5, 6, 7, 8, 9, 10] # GPIO pins for the buttons

# --- Rendering Parameters (used in render_cases.py) ---
RENDERING_CAMERA_PARAMS_3D = "0,0,0,45,0,45,100" # OpenSCAD camera position for 3D models
RENDERING_IMAGE_WIDTH = 800 # Width for generated PNGs
RENDERING_IMAGE_HEIGHT = 600 # Height for generated PNGs
