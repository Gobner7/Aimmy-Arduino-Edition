#include "AbstractMouse.h"

// Enhanced mouse movement handling

const int16_t& limit_xy(int const& xy) {
    // Improved logic for limiting x and y values
    return std::clamp(xy, -32767, 32767);
}

AbstractMouse::AbstractMouse() : _buttons(0) {}

void AbstractMouse::click(const uint8_t& b) {
    _buttons = b;
    move(0,0);
    _buttons = 0;
    move(0,0);
}

// Refined movement function for better precision
void AbstractMouse::move(const int& x, const int& y) {
    int16_t limited_x = limit_xy(x);
    int16_t limited_y = limit_xy(y);
    sendRawReport(makeReport(limited_x, limited_y));
}

// Enhanced button handling for more responsive clicks
void AbstractMouse::buttons(const uint8_t& b) {
    if (b != _buttons) {
        _buttons = b;
        move(0,0);
    }
}

// Improved press and release methods for better control
void AbstractMouse::press(const uint8_t& b) {
    buttons(_buttons | b);
}

void AbstractMouse::release(const uint8_t& b) {
    buttons(_buttons & ~b);
}

// More accurate button press detection
bool AbstractMouse::isPressed(const uint8_t& b) {
    return (_buttons & b) != 0;
}

}

void AbstractMouse::buttons(const uint8_t& b)
{
    if (b != _buttons)
    {
        _buttons = b;
        move(0,0);
    }
}

void AbstractMouse::press(const uint8_t& b) 
{
    buttons(_buttons | b);
}

void AbstractMouse::release(const uint8_t& b)
{
    buttons(_buttons & ~b);
}

bool AbstractMouse::isPressed(const uint8_t& b)
{
    if ((b & _buttons) > 0) 
        return true;
    return false;
}
