import os
import graphviz
from config import *

# --- Netlist Generation ---
def generate_button_pcb_netlist():
    netlist_fname = "button_pcb.net"
    
    # KiCad Netlist Header
    netlist_content = """(export (version D)
  (design
    (source "button_pcb.kicad_sch")
    (date "2023-10-27T10:00:00Z")
    (tool "script_generator")
  )
  (components
"""

    # ESP32 Connector (Generic 1x8 Pin Header)
    netlist_content += """    (comp (ref J1)
      (value Conn_01x08)
      (footprint Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm)
      (libsource (lib Connector_Generic) (part Conn_01x08) (description "Generic connector, single row, 01x08, script generated"))
      (sheetpath (names /) (tstamps /))
      (tstamp 00000000)
    )
"""

    # Buttons
    for i in range(NUM_BUTTONS):
        netlist_content += f"    (comp (ref SW{i+1})\n"
        netlist_content += f"      (value SW_Push)\n"
        netlist_content += f"      (footprint Button_SMD_6x6mm:SW_Push_6mm)\n"
        netlist_content += f"      (libsource (lib Button) (part SW_Push) (description \"Push button switch, generic, script generated\"))\n"
        netlist_content += f"      (sheetpath (names /) (tstamps /))\n"
        netlist_content += f"      (tstamp 0000000{i+1})\n"
        netlist_content += f"    )\n"

    netlist_content += "  )\n"
    netlist_content += "  (nets\n"

    # Connections
    for i in range(NUM_BUTTONS):
        # Button to GPIO
        netlist_content += f"    (net (code {i+1})\n"
        netlist_content += f"      (name \"Net-(J1-Pad{i+1})\")\n"
        netlist_content += f"      (node (ref J1) (pin {i+1}))\n"
        netlist_content += f"      (node (ref SW{i+1}) (pin 1))\n"
        netlist_content += f"    )\n"

    # Button to GND (assuming J1-Pin8 is GND)
    netlist_content += f"    (net (code {NUM_BUTTONS+1})\n"
    netlist_content += f"      (name \"GND\")\n"
        netlist_content += f"      (node (ref J1) (pin 8))\n"
    for i in range(NUM_BUTTONS):
        netlist_content += f"      (node (ref SW{i+1}) (pin 2))\n"
    netlist_content += "    )\n"

    netlist_content += "  )\n"
    netlist_content += ")\n"

    with open(netlist_fname, "w") as f:
        f.write(netlist_content)
    print(f"Generated KiCad netlist: {netlist_fname}")

# --- Conceptual Layout Generation ---
def generate_conceptual_layout():
    layout_fname = "button_pcb_layout.txt"
    with open(layout_fname, "w") as f:
        f.write("--- Conceptual Button PCB Layout ---\n\n")
        f.write(f"Board Dimensions (approx): {NUM_BUTTONS * BUTTON_SPACING + BUTTON_SPACING}mm x {BUTTON_SPACING * 2}mm\n\n")
        f.write("Button Placement (X, Y coordinates from bottom-left corner):\n")
        
        # Simple linear arrangement
        for i in range(NUM_BUTTONS):
            x_pos = (i * BUTTON_SPACING) + (BUTTON_SPACING / 2)
            y_pos = BUTTON_SPACING
            f.write(f"  Button {i+1}: ({x_pos:.1f}mm, {y_pos:.1f}mm)\n")
        
        f.write("\nConnections:\n")
        for i in range(NUM_BUTTONS):
            f.write(f"  Button {i+1} -> ESP32 GPIO{BUTTON_GPIO_PINS[i]} (via connector pin {i+1})\n")
        f.write(f"  All Buttons -> ESP32 GND (via connector pin 8)\n")

    print(f"Generated conceptual layout: {layout_fname}")

# --- Circuit Diagram Rendering ---
def render_circuit_diagram():
    dot = graphviz.Digraph(comment='Button PCB Circuit', format='png')
    dot.attr(rankdir='LR') # Left to Right layout

    # Add ESP32 Connector
    dot.node('J1', 'ESP32 Connector\n(J1)', shape='box')

    # Add Buttons
    for i in range(NUM_BUTTONS):
        dot.node(f'SW{i+1}', f'Button {i+1}\n(SW{i+1})', shape='box')

    # Add Connections
    for i in range(NUM_BUTTONS):
        # Button to GPIO
        dot.edge(f'SW{i+1}', 'J1', label=f'GPIO{BUTTON_GPIO_PINS[i]}')
        # Button to GND
        dot.edge(f'SW{i+1}', 'J1', label='GND')

    output_path = os.path.join("renderings", "button_circuit_diagram")
    dot.render(output_path, view=False, cleanup=True)
    print(f"Generated circuit diagram: {output_path}.png")

if __name__ == "__main__":
    generate_button_pcb_netlist()
    generate_conceptual_layout()
    render_circuit_diagram()