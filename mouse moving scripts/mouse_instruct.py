from enum import Enum
import hid

# Defining mouse buttons with clear constants
MOUSE_LEFT = 1
MOUSE_RIGHT = 2
MOUSE_MIDDLE = 4
MOUSE_ALL = MOUSE_LEFT | MOUSE_RIGHT | MOUSE_MIDDLE

class MouseInstruct:
    def __init__(self, dev):
        self._buttons_mask = 0
        self._dev = dev
        # Ensure the initial state is set to 0 movement
        self.move(0, 0)

    @classmethod
    def getMouse(cls, vid=0, pid=0, ping_code=0xf9):
        # Improved device search with explicit ping code verification
        dev = find_mouse_device(vid, pid, ping_code)
        if not dev:
            raise DeviceNotFoundError(f"Device with VID: {vid} & PID: {pid} not found.")
        return cls(dev)

    def _buttons(self, buttons):
        # Enhanced button state management
        if buttons != self._buttons_mask:
            self._buttons_mask = buttons
            self.move(0, 0)

    def click(self, button=MOUSE_LEFT):
        # Simulate click with press and release
        self.press(button)
        self.release(button)

    def press(self, button=MOUSE_LEFT):
        # Update button mask on press
        self._buttons(self._buttons_mask | button)

    def release(self, button=MOUSE_LEFT):
        # Update button mask on release
        self._buttons(self._buttons_mask & ~button)

    def is_pressed(self, button=MOUSE_LEFT):
        # Check if a specific button is pressed
        return bool(button & self._buttons_mask)

    def move(self, x, y):
        # Apply limit to x and y to prevent overflow
        limited_x = limit_xy(x)
        limited_y = limit_xy(y)
        # Construct and send the raw report for movement
        self._sendRawReport(self._makeReport(limited_x, limited_y))

    def _makeReport(self, x, y):
        # Generate report data with proper formatting
        report_data = [
            0x01,  # Report ID
            self._buttons_mask,
            low_byte(x), high_byte(x),
            low_byte(y), high_byte(y),
        ]
        return report_data

    def _sendRawReport(self, report_data):
        # Directly write the report data to the device
        self._dev.write(report_data)

class DeviceNotFoundError(Exception):
    # Custom exception for clearer error messaging
    pass

def check_ping(dev, ping_code):
    # Send ping and check for correct response
    dev.write([0, ping_code])
    resp = dev.read(max_length=1, timeout_ms=10)
    return resp and resp[0] == ping_code

def find_mouse_device(vid, pid, ping_code):
    # Enhanced device detection logic
    for dev_info in hid.enumerate(vid, pid):
        dev = hid.device()
        dev.open_path(dev_info['path'])
        if check_ping(dev, ping_code):
            return dev
        dev.close()
    return None

def limit_xy(xy):
    # Limit x and y values to valid range
    return max(min(xy, 32767), -32767)

def low_byte(x):
    # Extract low byte from integer
    return x & 0xFF

def high_byte(x):
    # Extract high byte from integer
    return (x >> 8) & 0xFF
    if xy < -32767:
        return -32767
    elif xy > 32767:
        return 32767
    else: return xy

def low_byte(x):
    return x & 0xFF

def high_byte(x):
    return (x >> 8) & 0xFF
