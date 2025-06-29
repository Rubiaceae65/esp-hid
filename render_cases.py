import subprocess
import os
import ezdxf

# Define paths
OUTPUT_DIR = "./renderings"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_openscad_model(scad_file, output_png, camera_params=None):
    print(f"Rendering {scad_file} to {output_png}...")
    command = ["openscad", "-o", output_png, scad_file]
    if camera_params:
        # Example camera_params: ["--camera=0,0,0,50,0,0,100"] (translate, rotate, distance)
        command.append(f"--camera={camera_params}")
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully rendered {output_png}")
    except FileNotFoundError:
        print("Error: OpenSCAD command not found. Please ensure OpenSCAD is installed and in your system's PATH.")
        print("Download from: https://openscad.org/downloads.html")
    except subprocess.CalledProcessError as e:
        print(f"Error rendering {scad_file}: {e.stderr}")

def convert_dxf_to_svg(dxf_file, output_svg):
    print(f"Converting {dxf_file} to {output_svg}...")
    try:
        doc = ezdxf.readfile(dxf_file)
        doc.saveas(output_svg)
        print(f"Successfully converted {output_svg}")
    except ezdxf.DXFStructureError:
        print(f"Error: Invalid DXF file: {dxf_file}")
    except Exception as e:
        print(f"Error converting {dxf_file} to SVG: {e}")

if __name__ == "__main__":
    # Render 3D printable case (OpenSCAD)
    render_openscad_model(
        "esp32_footswitch_case_base.scad", 
        os.path.join(OUTPUT_DIR, "esp32_footswitch_case_base.png"),
        camera_params="0,0,0,50,0,0,100" # Example camera position
    )
    render_openscad_model(
        "esp32_footswitch_case_lid.scad", 
        os.path.join(OUTPUT_DIR, "esp32_footswitch_case_lid.png"),
        camera_params="0,0,0,50,0,0,100" # Example camera position
    )

    # Convert laser-cut case (DXF) to SVG
    convert_dxf_to_svg("esp32_lasercut_case_top.dxf", os.path.join(OUTPUT_DIR, "esp32_lasercut_case_top.svg"))
    convert_dxf_to_svg("esp32_lasercut_case_bottom.dxf", os.path.join(OUTPUT_DIR, "esp32_lasercut_case_bottom.svg"))
    convert_dxf_to_svg("esp32_lasercut_case_front_back.dxf", os.path.join(OUTPUT_DIR, "esp32_lasercut_case_front_back.svg"))
    convert_dxf_to_svg("esp32_lasercut_case_left_right.dxf", os.path.join(OUTPUT_DIR, "esp32_lasercut_case_left_right.svg"))

    print("\nRendering script finished. Check the 'renderings/' directory.")
    print("For DXF to PNG conversion, you might need Inkscape: https://inkscape.org/")