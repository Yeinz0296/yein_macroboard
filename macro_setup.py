import time

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

SLEEP_TIME = 0.1
# Only for 1 char
def macro_setting(usb_keyboard, ble_keyboard, ble, usbLayout_keyboard, bleLayout_keyboard, usb_cc, ble_cc):
    def send_keycode(key):
        usb_keyboard.press(key)
        time.sleep(SLEEP_TIME)

        if ble.connected:
            ble_keyboard.press(key)
            time.sleep(SLEEP_TIME)
            ble_keyboard.release_all()
        usb_keyboard.release_all()

    # To send a string of texts/numbers
    def send_keylayout(texts):
        usbLayout_keyboard.write(texts)
        if ble.connected:
            bleLayout_keyboard.write(texts)
        time.sleep(0.4)

    def windows_short_cut(cmd):
        if cmd == 'lockScreen':
            usb_keyboard.send(Keycode.WINDOWS, Keycode.L)
        elif cmd == 'lockScreen':
            usb_keyboard.send(Keycode.WINDOWS, Keycode.L)
        else:
            print(f'Invalid Command: {cmd}')

    def multimedia_short_cut(cmd):
        if cmd == 'volumeUp':
            usb_cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            if ble.connected:
                ble_cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        elif cmd == 'volumeDown':
            usb_cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            if ble.connected:
                ble_cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        elif cmd == 'mute':
            usb_cc.send(ConsumerControlCode.MUTE)
            if ble.connected:
                ble_cc.send(ConsumerControlCode.MUTE)
        elif cmd == 'playPause':
            usb_cc.send(ConsumerControlCode.PLAY_PAUSE)
            if ble.connected:
                ble_cc.send(ConsumerControlCode.PLAY_PAUSE)
        elif cmd == 'stop':
            usb_cc.send(ConsumerControlCode.STOP)
            if ble.connected:
                ble_cc.send(ConsumerControlCode.STOP)
        else:
            print(f'Invalid Command: {cmd}')

    return send_keycode, send_keylayout, windows_short_cut, multimedia_short_cut
