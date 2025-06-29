import os
from solid import *
from solid.utils import *
from solid.solidpython import scad_render
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.svg import SVGBackend
from ezdxf.addons.drawing.layout import Page, Units

# Import case generation scripts to reuse parameters and functions
# We'll re-define parameters here for clarity and to avoid circular imports if needed

# Case parameters (from generate_case.py and generate_lasercut_case.py)
CASE_LENGTH = 150
CASE_WIDTH = 100
CASE_HEIGHT = 30
WALL_THICKNESS = 2
MATERIAL_THICKNESS = 3 # For laser cutting

BOARD_LENGTH = 34.3
BOARD_WIDTH = 25.4

FOOTSWITCH_MOUNT_DIAMETER = 12
FOOTSWITCH_CAP_DIAMETER = 16
FOOTSWITCH_DEPTH = 20

BUTTON_HOLE_DIAMETER = 6
BUTTON_SPACING = 15

USB_C_WIDTH = 10
USB_C_HEIGHT = 5
USB_C_DEPTH = 7
USB_C_OFFSET_FROM_BOTTOM = 5

LED_HOLE_DIAMETER = 3
LED_OFFSET_X = 10
LED_OFFSET_Y = 10

BOARD_STANDOFF_DIAMETER = 4
BOARD_STANDOFF_HEIGHT = 5
BOARD_STANDOFF_SCREW_DIAMETER = 2.5

SCREW_DIAMETER = 3.2
SCREW_OFFSET = 5
SCREW_HEAD_DIAMETER = 6
SCREW_HOLE_DEPTH = 5
LID_SCREW_STANDOFF_HEIGHT = 5

# --- BOM Generation ---
def generate_bom():
    bom = {
        "ESP32-S3 LOLIN S3 Mini": {"quantity": 1, "notes": "Main microcontroller board"},
        "Momentary Footswitches": {"quantity": 7, "notes": "For keyboard/mouse inputs"},
        "M3 Screws (for case assembly)": {"quantity": 4, "notes": f"Length depends on LID_SCREW_STANDOFF_HEIGHT ({LID_SCREW_STANDOFF_HEIGHT}mm) + WALL_THICKNESS ({WALL_THICKNESS}mm)"},
        "M2.5 or M3 Screws (for board mounting)": {"quantity": 4, "notes": f"Length depends on BOARD_STANDOFF_HEIGHT ({BOARD_STANDOFF_HEIGHT}mm)"},
        "Wires": {"quantity": "~2 meters", "notes": "For connecting buttons to ESP32"},
        "Acrylic Sheet (for laser cut case)": {"quantity": "See material usage", "notes": f"Thickness: {MATERIAL_THICKNESS}mm"},
        "PLA/PETG Filament (for 3D printed case)": {"quantity": "See material usage", "notes": ""},
    }
    return bom

# --- 3D Printing Estimates ---

def calculate_3d_print_estimates():
    # Calculate volume of base part
    base_outer_volume = CASE_LENGTH * CASE_WIDTH * (CASE_HEIGHT / 2) # Outer dimensions of base part
    base_inner_hollow_volume = (CASE_LENGTH - 2 * WALL_THICKNESS) * (CASE_WIDTH - 2 * WALL_THICKNESS) * (CASE_HEIGHT / 2 - WALL_THICKNESS)
    usb_cutout_volume = USB_C_WIDTH * (WALL_THICKNESS + 0.1) * USB_C_HEIGHT # Approximate volume of USB cutout
    
    # Standoffs volume (approximate as solid cylinders)
    standoff_volume = 4 * (3.14159 * (BOARD_STANDOFF_DIAMETER / 2)**2 * BOARD_STANDOFF_HEIGHT)
    lid_screw_standoff_volume = 4 * (3.14159 * (SCREW_HEAD_DIAMETER / 2)**2 * LID_SCREW_STANDOFF_HEIGHT)

    # Calculate volume of lid part
    lid_outer_volume = CASE_LENGTH * CASE_WIDTH * (CASE_HEIGHT / 2) # Outer dimensions of lid part
    lid_inner_hollow_volume = (CASE_LENGTH - 2 * WALL_THICKNESS) * (CASE_WIDTH - 2 * WALL_THICKNESS) * (CASE_HEIGHT / 2 - WALL_THICKNESS)
    footswitch_hole_volume = 7 * (3.14159 * (FOOTSWITCH_MOUNT_DIAMETER / 2)**2 * (WALL_THICKNESS + FOOTSWITCH_DEPTH))
    led_hole_volume = 3.14159 * (LED_HOLE_DIAMETER / 2)**2 * (WALL_THICKNESS + 0.1)
    lid_screw_through_hole_volume = 4 * (3.14159 * (SCREW_DIAMETER / 2)**2 * (WALL_THICKNESS + 0.1))

    # Approximate material volume for base and lid
    # This is a simplified approach assuming a certain infill for the main body and solid features
    infill_percentage = 0.20 # 20% infill

    # Volume of the main hollowed out parts
    base_hollow_volume = base_outer_volume - base_inner_hollow_volume - usb_cutout_volume
    lid_hollow_volume = lid_outer_volume - lid_inner_hollow_volume - footswitch_hole_volume - led_hole_volume - lid_screw_through_hole_volume

    # Total material volume
    total_material_volume_mm3 = (base_hollow_volume + lid_hollow_volume) * infill_percentage + standoff_volume + lid_screw_standoff_volume

    # Rough estimates
    filament_density_g_mm3 = 1.24e-3 # PLA density (g/mm^3)
    filament_cost_per_kg = 20 # USD
    printing_speed_mm3_s = 20 # Very rough average printing speed

    total_weight_g = total_material_volume_mm3 * filament_density_g_mm3
    total_cost_usd = (total_weight_g / 1000) * filament_cost_per_kg
    estimated_print_time_hours = (total_material_volume_mm3 / printing_speed_mm3_s) / 3600

    return {
        "total_volume_mm3": total_material_volume_mm3,
        "total_weight_g": total_weight_g,
        "total_cost_usd": total_cost_usd,
        "estimated_print_time_hours": estimated_print_time_hours
    }

# --- Laser Cutting Estimates ---

def calculate_laser_cut_estimates():
    # For laser cutting, we're interested in the area of each panel
    # and the total cut length (very rough estimate based on perimeter)

    panels = {
        "top": {"width": CASE_LENGTH, "height": CASE_WIDTH},
        "bottom": {"width": CASE_LENGTH, "height": CASE_WIDTH},
        "front_back": {"width": CASE_LENGTH, "height": CASE_HEIGHT},
        "left_right": {"width": CASE_WIDTH, "height": CASE_HEIGHT},
    }

    total_area_mm2 = 0
    total_perimeter_mm = 0

    for name, dims in panels.items():
        area = dims["width"] * dims["height"]
        perimeter = 2 * (dims["width"] + dims["height"])
        total_area_mm2 += area
        total_perimeter_mm += perimeter

    # Rough estimates for laser cutting
    laser_cut_speed_mm_s = 10 # Very rough average cutting speed
    acrylic_cost_per_mm2 = 0.0001 # Very rough cost per mm^2 for 3mm acrylic

    total_cost_usd = total_area_mm2 * acrylic_cost_per_mm2
    estimated_cut_time_minutes = (total_perimeter_mm / laser_cut_speed_mm_s) / 60

    return {
        "total_area_mm2": total_area_mm2,
        "total_perimeter_mm": total_perimeter_mm,
        "total_cost_usd": total_cost_usd,
        "estimated_cut_time_minutes": estimated_cut_time_minutes
    }

if __name__ == "__main__":
    print("\n--- Bill of Materials ---")
    bom = generate_bom()
    for item, details in bom.items():
        print(f"- {item}: {details['quantity']} ({details['notes']})")

    print("\n--- 3D Printing Estimates (Rough) ---")
    print_estimates = calculate_3d_print_estimates()
    print(f"  Total Volume: {print_estimates['total_volume_mm3']:.2f} mm^3")
    print(f"  Estimated Filament Weight: {print_estimates['total_weight_g']:.2f} g")
    print(f"  Estimated Filament Cost: ${print_estimates['total_cost_usd']:.2f}")
    print(f"  Estimated Print Time: {print_estimates['estimated_print_time_hours']:.2f} hours")
    print("  (Note: These are very rough estimates. Use a slicer for accuracy.)")

    print("\n--- Laser Cutting Estimates (Rough) ---")
    laser_estimates = calculate_laser_cut_estimates()
    print(f"  Total Material Area: {laser_estimates['total_area_mm2']:.2f} mm^2")
    print(f"  Total Cut Length (approx): {laser_estimates['total_perimeter_mm']:.2f} mm")
    print(f"  Estimated Acrylic Cost: ${laser_estimates['total_cost_usd']:.2f}")
    print(f"  Estimated Cut Time: {laser_estimates['estimated_cut_time_minutes']:.2f} minutes")
    print("  (Note: These are very rough estimates. Use laser cutter software for accuracy.)")