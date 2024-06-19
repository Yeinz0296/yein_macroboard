import time
import board
import digitalio
import rotaryio
import usb_hid
import pwmio
import displayio
import terminalio
from board_setup import *
from macro_setup import macro_setting
import adafruit_displayio_sh1106
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService

displayio.release_displays()
# var
SLEEP_TIME = 0.1
connected_flag = False
current_layer = 1
last_layer_button_state = buttons[board.D0].value

# BLE and USB HID setup
hid = HIDService()
usb_keyboard = Keyboard(usb_hid.devices)
ble_keyboard = Keyboard(hid.devices)
usbLayout_keyboard = KeyboardLayoutUS(usb_keyboard)
bleLayout_keyboard = KeyboardLayoutUS(ble_keyboard)
usb_cc = ConsumerControl(usb_hid.devices)
ble_cc = ConsumerControl(hid.devices)

# BLE setup
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
ble = BLERadio()
ble.name = "yein's macroboard"

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=128, height=64, rotation=0)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000  # Black

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

send_keycode, send_keylayout, windows_short_cut, multimedia_short_cut = macro_setting(
    usb_keyboard,
    ble_keyboard,
    ble,
    usbLayout_keyboard,
    bleLayout_keyboard,
    usb_cc,
    ble_cc,
)
def display_text(oledText):
    text_area = label.Label(terminalio.FONT, text=oledText,color=0xFFFFFF, x=28, y=15)
    splash.append(text_area)

# Normal shortcut layer
def layer1():
    splash.append(bg_sprite)
    display_text("Layer 1")

    #if not buttons[board.D1].value:
    #    send_keycode(Keycode.A)
    #if not buttons[board.D2].value and not buttons[board.D3].value:
    #    send_keylayout("0296")

# Multimedia Layer
last_position = encoder.position
def layer2():
    splash.append(bg_sprite)
    display_text("Layer 2")
    global last_position
    current_position = encoder.position
    position_change = current_position - last_position

    if position_change > 0:
        for _ in range(position_change):
            multimedia_short_cut("volumeUp")
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            multimedia_short_cut("volumeDown")
        print(current_position)
    last_position = current_position
    if not buttons[board.D3].value:
        multimedia_short_cut("mute")

# Windows manager layer
def layer3():
    splash.append(bg_sprite)
    display_text("Layer 3")
    #if not buttons[board.D1].value:
    #    windows_short_cut("lockScreen")

def macroSetup():
    global current_layer
    global last_layer_button_state
    redLed.value = True
    blueLed.value = True
    greenLed.value = True

    if buttons[board.D0].value != last_layer_button_state and not buttons[board.D0].value:
        current_layer = (current_layer % 3) + 1
        print(f'Switched to layer {current_layer}')
    last_layer_button_state = buttons[board.D0].value

    if current_layer == 1:
        redLed.value = False
        layer1()
    if current_layer == 2:
        blueLed.value = False
        layer2()
    if current_layer == 3:
        greenLed.value = False
        layer3()
    if current_layer == 4:
        redLed.value = False
        greenLed.value = False
    if current_layer == 5:
        redLed.value = False
        blueLed.value = False
    if current_layer == 6:
        greenLed.value = False
        blueLed.value = False
    if current_layer == 7:
        redLed.value = False
        greenLed.value = False
        blueLed.value = False
    time.sleep(SLEEP_TIME)

if not ble.connected:
    print("Waiting to connect to BLE...")
    ble.start_advertising(advertisement)
else:
    print("already connected")

def main():
    try:
        print(f'Screen is {display.is_awake}')
        while len(splash):
            splash.pop()
        macroSetup()
    except Exception as e:
        print("An error occurred:", str(e))
        time.sleep(1)

if __name__ == "__main__":
    while True:
        main()
