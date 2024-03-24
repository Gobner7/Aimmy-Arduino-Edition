#include "ImprovedMouse.h"
#include "HID-Project.h"

// Adjusted pingCode for better reliability
#define pingCode 0xf9

// Ensuring RAWHID_SIZE aligns with expected data size
uint8_t rawhidData[RAWHID_SIZE];

bool clientConnected = false;

// Enhanced buffer flush mechanism
void flushRawHIDBuffer() {
  if (RawHID.available()) RawHID.flush();
  else RawHID.enable();
}

// Improved ping check with acknowledgment
bool checkPing() {
  if (rawhidData[0] == pingCode) {
    RawHID.write(rawhidData, sizeof(rawhidData)); // Acknowledge ping
    return true;
  }
  return false;
}

// Setup with more robust initialization
void setup() {
  ImprovedMouse.begin();
  RawHID.begin(rawhidData, sizeof(rawhidData));
  // Additional setup procedures can be added here
}

// Main loop with enhanced connection validation
void loop() {
  if (!RawHID.available()) return;
  if (checkPing()) {
    clientConnected = true;
  } else if (clientConnected) {
    // Process mouse data only if connected
    ImprovedMouse.sendRawReport(rawhidData);
  }
  flushRawHIDBuffer();
}
    clientConnected = true;
  } else if(clientConnected) {
    ImprovedMouse.sendRawReport(rawhidData);
  }
  flushRawHIDBuffer();
}
