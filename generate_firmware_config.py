import os
from config import *

def generate_firmware_config_h():
    config_h_content = """
#ifndef CONFIG_H
#define CONFIG_H

// Auto-generated from config.py

// Firmware Parameters
#define PIN_ENTER {}
#define PIN_ESC {}
#define PIN_PAGE_UP {}
#define PIN_PAGE_DOWN {}
#define PIN_MACRO_1 {}
#define PIN_MACRO_2 {}
#define PIN_MACRO_3 {}
#define PIN_LED {}

#define DEBOUNCE_MS {}

#define BLE_KEYBOARD_NAME "{}"
#define BLE_MOUSE_NAME "{}"

#define MACRO_1_OUTPUT "{}"
#define MACRO_2_OUTPUT "{}"
#define MACRO_3_OUTPUT "{}"

#endif // CONFIG_H
""".format(
        PIN_ENTER,
        PIN_ESC,
        PIN_PAGE_UP,
        PIN_PAGE_DOWN,
        PIN_MACRO_1,
        PIN_MACRO_2,
        PIN_MACRO_3,
        PIN_LED,
        DEBOUNCE_MS,
        BLE_KEYBOARD_NAME,
        BLE_MOUSE_NAME,
        MACRO_1_OUTPUT,
        MACRO_2_OUTPUT,
        MACRO_3_OUTPUT
    )

    with open("config.h", "w") as f:
        f.write(config_h_content)
    print("Generated config.h")

if __name__ == "__main__":
    generate_firmware_config_h()
