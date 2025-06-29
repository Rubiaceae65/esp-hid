.PHONY: all firmware 3d_case lasercut_case renderings clean

# Define Python interpreter from the virtual environment
PYTHON := ./venv/bin/python

# Project directories
SRC_DIR := src
LIB_DIR := lib
RENDERINGS_DIR := renderings

# Generated files
SCAD_BASE := esp32_footswitch_case_base.scad
SCAD_LID := esp32_footswitch_case_lid.scad
DXF_TOP := esp32_lasercut_case_top.dxf
DXF_BOTTOM := esp32_lasercut_case_bottom.dxf
DXF_FRONT_BACK := esp32_lasercut_case_front_back.dxf
DXF_LEFT_RIGHT := esp32_lasercut_case_left_right.dxf
RENDER_BASE_PNG := $(RENDERINGS_DIR)/esp32_footswitch_case_base.png
RENDER_LID_PNG := $(RENDERINGS_DIR)/esp32_footswitch_case_lid.png
RENDER_LASERCUT_TOP_SVG := $(RENDERINGS_DIR)/esp32_lasercut_case_top.svg
RENDER_LASERCUT_BOTTOM_SVG := $(RENDERINGS_DIR)/esp32_lasercut_case_bottom.svg
RENDER_LASERCUT_FRONT_BACK_SVG := $(RENDERINGS_DIR)/esp32_lasercut_case_front_back.svg
RENDER_LASERCUT_LEFT_RIGHT_SVG := $(RENDERINGS_DIR)/esp32_lasercut_case_left_right.svg

# Default target: build firmware and generate all case files and renderings
all: firmware 3d_case lasercut_case renderings

# Target to build the ESP32 firmware
firmware:
	@echo "Building firmware..."
	/home/user/.local/bin/pio run

# Target to generate 3D printable case files (.scad)
3d_case: generate_case.py
	@echo "Generating 3D printable case files..."
	$(PYTHON) generate_case.py

# Target to generate laser-cut case files (.dxf)
lasercut_case: generate_lasercut_case.py
	@echo "Generating laser-cut case files..."
	$(PYTHON) generate_lasercut_case.py

# Target to generate image renderings for the README
renderings: $(RENDERINGS_DIR) $(SCAD_BASE) $(SCAD_LID) $(DXF_TOP) $(DXF_BOTTOM) $(DXF_FRONT_BACK) $(DXF_LEFT_RIGHT) render_cases.py
	@echo "Generating case renderings..."
	$(PYTHON) render_cases.py

# Create renderings directory if it doesn't exist
$(RENDERINGS_DIR):
	mkdir -p $(RENDERINGS_DIR)

# Target to clean up generated files
clean:
	@echo "Cleaning up generated files..."
	rm -f $(SCAD_BASE) $(SCAD_LID)
	rm -f $(DXF_TOP) $(DXF_BOTTOM) $(DXF_FRONT_BACK) $(DXF_LEFT_RIGHT)
	rm -rf $(RENDERINGS_DIR)
	/home/user/.local/bin/pio run --target clean
	rm -rf venv
