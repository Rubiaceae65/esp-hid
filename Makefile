.PHONY: all firmware 3d_case lasercut_case renderings bom_estimates pcb_design clean venv_setup

# Define Python interpreter from the virtual environment
PYTHON := ./venv/bin/python

# Project directories
SRC_DIR := src
LIB_DIR := lib
RENDERINGS_DIR := renderings
VENV_DIR := venv

# Generated files
SCAD_BASE := esp32_footswitch_case_base.scad
SCAD_LID := esp32_footswitch_case_lid.scad
DXF_TOP := esp32_lasercut_case_top.dxf
DXF_BOTTOM := esp32_lasercut_case_bottom.dxf
DXF_FRONT_BACK := esp32_lasercut_case_front_back.dxf
DXF_LEFT_RIGHT := esp32_lasercut_case_left_right.dxf
NETLIST_FILE := button_pcb.net
LAYOUT_FILE := button_pcb_layout.txt
CONFIG_H := config.h

# Default target: build firmware and generate all case files and renderings
all: $(VENV_DIR) firmware 3d_case lasercut_case renderings bom_estimates pcb_design

# Target to set up the Python virtual environment and install dependencies
$(VENV_DIR):
	@echo "Setting up Python virtual environment and installing dependencies..."
	python3 -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip setuptools
	$(PYTHON) -m pip install solidpython ezdxf Pillow graphviz

# Target to build the ESP32 firmware
firmware: $(CONFIG_H)
	@echo "Building firmware..."
	/home/user/.local/bin/pio run

# Target to generate config.h
$(CONFIG_H): generate_firmware_config.py config.py $(VENV_DIR)
	@echo "Generating firmware config header..."
	$(PYTHON) generate_firmware_config.py

# Target to generate 3D printable case files (.scad)
3d_case: generate_case.py config.py $(VENV_DIR)
	@echo "Generating 3D printable case files..."
	$(PYTHON) generate_case.py

# Target to generate laser-cut case files (.dxf)
lasercut_case: generate_lasercut_case.py config.py $(VENV_DIR)
	@echo "Generating laser-cut case files..."
	$(PYTHON) generate_lasercut_case.py

# Target to generate image renderings for the README
renderings: $(RENDERINGS_DIR) $(SCAD_BASE) $(SCAD_LID) $(DXF_TOP) $(DXF_BOTTOM) $(DXF_FRONT_BACK) $(DXF_LEFT_RIGHT) render_cases.py config.py $(VENV_DIR)
	@echo "Generating case renderings..."
	$(PYTHON) render_cases.py

# Target to generate BOM and estimates
bom_estimates: generate_bom_and_estimates.py config.py $(VENV_DIR)
	@echo "Generating BOM and estimates..."
	$(PYTHON) generate_bom_and_estimates.py

# Target to generate PCB design files
pcb_design: generate_button_pcb.py config.py $(VENV_DIR)
	@echo "Generating PCB design files..."
	$(PYTHON) generate_button_pcb.py

# Create renderings directory if it doesn't exist
$(RENDERINGS_DIR):
	mkdir -p $(RENDERINGS_DIR)

# Target to clean up generated files
clean:
	@echo "Cleaning up generated files..."
	rm -f $(SCAD_BASE) $(SCAD_LID)
	rm -f $(DXF_TOP) $(DXF_BOTTOM) $(DXF_FRONT_BACK) $(DXF_LEFT_RIGHT)
	rm -f $(NETLIST_FILE) $(LAYOUT_FILE) $(CONFIG_H)
	rm -rf $(RENDERINGS_DIR)
	/home/user/.local/bin/pio run --target clean
	rm -rf $(VENV_DIR)
