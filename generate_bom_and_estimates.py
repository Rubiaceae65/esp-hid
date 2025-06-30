import os
from solid import *
from solid.utils import *
from solid.solidpython import scad_render
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.svg import SVGBackend
from ezdxf.addons.drawing.layout import Page, Units
import config

# --- BOM Generation ---
def generate_bom():
    bom = {
        "ESP32-S3 LOLIN S3 Mini": {"quantity": 1, "notes": "Main microcontroller board", "price_per_unit": "", "shop_link": ""},
        "Momentary Footswitches": {"quantity": config.NUM_BUTTONS, "notes": "For keyboard/mouse inputs", "price_per_unit": "", "shop_link": ""},
        "M3 Screws (for case assembly)": {"quantity": 4, "notes": f"Length depends on LID_SCREW_STANDOFF_HEIGHT ({config.LID_SCREW_STANDOFF_HEIGHT}mm) + WALL_THICKNESS ({config.WALL_THICKNESS}mm)", "price_per_unit": "", "shop_link": ""},
        "M2.5 or M3 Screws (for board mounting)": {"quantity": 4, "notes": f"Length depends on BOARD_STANDOFF_HEIGHT ({config.BOARD_STANDOFF_HEIGHT}mm)", "price_per_unit": "", "shop_link": ""},
        "Wires": {"quantity": "~2 meters", "notes": "For connecting buttons to ESP32", "price_per_unit": "", "shop_link": ""},
        "Acrylic Sheet (for laser cut case)": {"quantity": "See material usage", "notes": f"Thickness: {config.MATERIAL_THICKNESS}mm", "price_per_unit": "", "shop_link": ""},
        "PLA/PETG Filament (for 3D printed case)": {"quantity": "See material usage", "notes": "", "price_per_unit": "", "shop_link": ""},
    }
    return bom

# --- 3D Printing Estimates ---

def calculate_3d_print_estimates():
    # Calculate volume of base part
    base_outer_volume = config.CASE_LENGTH * config.CASE_WIDTH * (config.CASE_HEIGHT / 2) # Outer dimensions of base part
    base_inner_hollow_volume = (config.CASE_LENGTH - 2 * config.WALL_THICKNESS) * (config.CASE_WIDTH - 2 * config.WALL_THICKNESS) * (config.CASE_HEIGHT / 2 - config.WALL_THICKNESS)
    usb_cutout_volume = config.USB_C_WIDTH * (config.WALL_THICKNESS + 0.1) * config.USB_C_HEIGHT # Approximate volume of USB cutout
    
    # Standoffs volume (approximate as solid cylinders)
    standoff_volume = 4 * (3.14159 * (config.BOARD_STANDOFF_DIAMETER / 2)**2 * config.BOARD_STANDOFF_HEIGHT)
    lid_screw_standoff_volume = 4 * (3.14159 * (config.SCREW_HEAD_DIAMETER / 2)**2 * config.LID_SCREW_STANDOFF_HEIGHT)

    # Calculate volume of lid part
    lid_outer_volume = config.CASE_LENGTH * config.CASE_WIDTH * (config.CASE_HEIGHT / 2) # Outer dimensions of lid part
    lid_inner_hollow_volume = (config.CASE_LENGTH - 2 * config.WALL_THICKNESS) * (config.CASE_WIDTH - 2 * config.WALL_THICKNESS) * (config.CASE_HEIGHT / 2 - config.WALL_THICKNESS)
    footswitch_hole_volume = config.NUM_BUTTONS * (3.14159 * (config.FOOTSWITCH_MOUNT_DIAMETER / 2)**2 * (config.WALL_THICKNESS + config.FOOTSWITCH_DEPTH))
    led_hole_volume = 3.14159 * (config.LED_HOLE_DIAMETER / 2)**2 * (config.WALL_THICKNESS + 0.1)
    lid_screw_through_hole_volume = 4 * (3.14159 * (config.SCREW_DIAMETER / 2)**2 * (config.WALL_THICKNESS + 0.1))

    # Approximate material volume for base and lid
    # This is a simplified approach assuming a certain infill for the main body and solid features

    # Volume of the main hollowed out parts
    base_hollow_volume = base_outer_volume - base_inner_hollow_volume - usb_cutout_volume
    lid_hollow_volume = lid_outer_volume - lid_inner_hollow_volume - footswitch_hole_volume - led_hole_volume - lid_screw_through_hole_volume

    # Total material volume
    total_material_volume_mm3 = (base_hollow_volume + lid_hollow_volume) * config.INFILL_PERCENTAGE + standoff_volume + lid_screw_standoff_volume

    # Rough estimates
    total_weight_g = total_material_volume_mm3 * config.FILAMENT_DENSITY_G_MM3
    total_cost_usd = (total_weight_g / 1000) * config.FILAMENT_COST_PER_KG
    estimated_print_time_hours = (total_material_volume_mm3 / config.PRINTING_SPEED_MM3_S) / 3600

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
        "top": {"width": config.CASE_LENGTH, "height": config.CASE_WIDTH},
        "bottom": {"width": config.CASE_LENGTH, "height": config.CASE_WIDTH},
        "front_back": {"width": config.CASE_LENGTH, "height": config.CASE_HEIGHT},
        "left_right": {"width": config.CASE_WIDTH, "height": config.CASE_HEIGHT},
    }

    total_area_mm2 = 0
    total_perimeter_mm = 0

    for name, dims in panels.items():
        area = dims["width"] * dims["height"]
        perimeter = 2 * (dims["width"] + dims["height"])
        total_area_mm2 += area
        total_perimeter_mm += perimeter

    # Rough estimates for laser cutting
    total_cost_usd = total_area_mm2 * config.ACRYLIC_COST_PER_MM2
    estimated_cut_time_minutes = (total_perimeter_mm / config.LASER_CUT_SPEED_MM_S) / 60

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
