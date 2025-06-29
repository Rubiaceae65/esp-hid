#include <Arduino.h>
#include "config.h"

#pragma message("config.h included!")

#include "USB.h"
#include "USBHIDMouse.h"
#include <BleKeyboard.h>
#include <BleMouse.h>

// Pin definitions for buttons
// All PIN definitions are now in config.h

// Button state and debounce
struct Button {
    const uint8_t PIN;
    uint32_t number;
    bool last_stable_state; // Last confirmed stable state (true for released, false for pressed)
    unsigned long last_debounce_time; // Last time the raw state changed
    bool pressed; // True if button is currently considered pressed (debounced)
};

Button buttons[] = {
    {PIN_ENTER, 1, true, 0, false},
    {PIN_ESC, 2, true, 0, false},
    {PIN_PAGE_UP, 3, true, 0, false},
    {PIN_PAGE_DOWN, 4, true, 0, false},
    {PIN_MACRO_1, 5, true, 0, false},
    {PIN_MACRO_2, 6, true, 0, false},
    {PIN_MACRO_3, 7, true, 0, false}
};

// DEBOUNCE_MS is now in config.h

BleKeyboard bleKeyboard(BLE_KEYBOARD_NAME);
BleMouse bleMouse(BLE_MOUSE_NAME);

#include "USBHIDKeyboard.h"
#include "USBHIDGamepad.h"
#include "USBHIDConsumerControl.h"
#include "USBHIDSystemControl.h"

USBCDC USBSerial;

USBHID HID;
USBHIDKeyboard Keyboard;
USBHIDMouse Mouse;
USBHIDGamepad Gamepad;
USBHIDConsumerControl ConsumerControl;
USBHIDSystemControl SystemControl;

const int buttonPin = 0;
int previousButtonState = HIGH;

static void usbEventCallback(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data) {
  if (event_base == ARDUINO_USB_EVENTS) {
    arduino_usb_event_data_t *data = (arduino_usb_event_data_t *)event_data;
    switch (event_id) {
      case ARDUINO_USB_STARTED_EVENT: Serial.println("USB PLUGGED"); break;
      case ARDUINO_USB_STOPPED_EVENT: Serial.println("USB UNPLUGGED"); break;
      case ARDUINO_USB_SUSPEND_EVENT: Serial.printf("USB SUSPENDED: remote_wakeup_en: %u\n", data->suspend.remote_wakeup_en); break;
      case ARDUINO_USB_RESUME_EVENT:  Serial.println("USB RESUMED"); break;

      default: break;
    }
  } else if (event_base == ARDUINO_USB_CDC_EVENTS) {
    arduino_usb_cdc_event_data_t *data = (arduino_usb_cdc_event_data_t *)event_data;
    switch (event_id) {
      case ARDUINO_USB_CDC_CONNECTED_EVENT:    Serial.println("CDC CONNECTED"); break;
      case ARDUINO_USB_CDC_DISCONNECTED_EVENT: Serial.println("CDC DISCONNECTED"); break;
      case ARDUINO_USB_CDC_LINE_STATE_EVENT:   Serial.printf("CDC LINE STATE: dtr: %u, rts: %u\n", data->line_state.dtr, data->line_state.rts); break;
      case ARDUINO_USB_CDC_LINE_CODING_EVENT:
        Serial.printf(
          "CDC LINE CODING: bit_rate: %lu, data_bits: %u, stop_bits: %u, parity: %u\n", data->line_coding.bit_rate, data->line_coding.data_bits,
          data->line_coding.stop_bits, data->line_coding.parity
        );
        break;
      case ARDUINO_USB_CDC_RX_EVENT:
        Serial.printf("CDC RX [%u]:", data->rx.len);
        {
          uint8_t buf[data->rx.len];
          size_t len = USBSerial.read(buf, data->rx.len);
          Serial.write(buf, len);
        }
        Serial.println();
        break;
      case ARDUINO_USB_CDC_RX_OVERFLOW_EVENT: Serial.printf("CDC RX Overflow of %d bytes", data->rx_overflow.dropped_bytes); break;

      default: break;
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Setup buttons
  for (auto& btn : buttons) {
      pinMode(btn.PIN, INPUT_PULLUP);
  }

  // Setup LED
  pinMode(PIN_LED, OUTPUT);

  // Start BLE
  bleKeyboard.begin();
  bleMouse.begin();

  USB.onEvent(usbEventCallback);
  USBSerial.onEvent(usbEventCallback);
  HID.onEvent(usbEventCallback);
  Keyboard.onEvent(usbEventCallback);

  USBSerial.begin();
  Mouse.begin();
  Keyboard.begin();
  Gamepad.begin();
  ConsumerControl.begin();
  SystemControl.begin();
  USB.begin();

  Serial.println("ESP32-S3 HID device started");

  // Indicate successful boot by flashing the LED
  for (int i = 0; i < 5; i++) {
      digitalWrite(PIN_LED, HIGH);
      delay(100);
      digitalWrite(PIN_LED, LOW);
      delay(100);
  }
}

void handle_buttons() {
    for (auto& btn : buttons) {
        bool reading = (digitalRead(btn.PIN) == LOW); // LOW means pressed

        if (reading != btn.last_stable_state) {
            btn.last_debounce_time = millis();
        }

        if ((millis() - btn.last_debounce_time) > DEBOUNCE_MS) {
            if (reading != btn.pressed) {
                btn.pressed = reading;
                if (btn.pressed) {
                    Serial.printf("Button %d pressed\n", btn.number);

                    if (bleKeyboard.isConnected()) {
                        switch (btn.PIN) {
                            case PIN_ENTER: bleKeyboard.write(KEY_RETURN); break;
                            case PIN_ESC: bleKeyboard.write(KEY_ESC); break;
                            case PIN_PAGE_UP: bleKeyboard.write(KEY_PAGE_UP); break;
                            case PIN_PAGE_DOWN: bleKeyboard.write(KEY_PAGE_DOWN); break;
                            case PIN_MACRO_1: bleKeyboard.print(MACRO_1_OUTPUT); break;
                            case PIN_MACRO_2: bleKeyboard.print(MACRO_2_OUTPUT); break;
                            case PIN_MACRO_3: bleKeyboard.print(MACRO_3_OUTPUT); break;
                        }
                    } else if (HID.ready()) {
                        switch (btn.PIN) {
                            case PIN_ENTER: Keyboard.write(KEY_RETURN); break;
                            case PIN_ESC: Keyboard.write(KEY_ESC); break;
                            case PIN_PAGE_UP: Keyboard.write(KEY_PAGE_UP); break;
                            case PIN_PAGE_DOWN: Keyboard.write(KEY_PAGE_DOWN); break;
                            case PIN_MACRO_1: Keyboard.print(MACRO_1_OUTPUT); break;
                            case PIN_MACRO_2: Keyboard.print(MACRO_2_OUTPUT); break;
                            case PIN_MACRO_3: Keyboard.print(MACRO_3_OUTPUT); break;
                        }
                    }
                }
            }
        }
        btn.last_stable_state = reading;
    }
}

void loop() {
  handle_buttons();

  /*
  static unsigned long last_action_time = 0;
  const unsigned long action_interval = 10000; // 10 seconds

  if (millis() - last_action_time > action_interval) {
      last_action_time = millis();
      Serial.println("Performing automated action...");

      if (bleKeyboard.isConnected()) {
          bleKeyboard.print("Hello from ESP32-S3! ");
          bleMouse.move(5, 0, 0, 0);
          delay(100);
          bleMouse.move(0, 5, 0, 0);
          delay(100);
          bleMouse.move(-5, 0, 0, 0);
          delay(100);
          bleMouse.move(0, -5, 0, 0);
      } else if (HID.ready()) {
          Keyboard.print("Hello from ESP32-S3! ");
          Mouse.move(5, 0, 0, 0);
          delay(100);
          Mouse.move(0, 5, 0, 0);
          delay(100);
          Mouse.move(-5, 0, 0, 0);
          delay(100);
          Mouse.move(0, -5, 0, 0);
      }
  }
  */

  if (bleKeyboard.isConnected()) {
      digitalWrite(PIN_LED, HIGH);
  } else {
      digitalWrite(PIN_LED, LOW);
  }

  delay(10);
}