import board
import digitalio
import rotaryio

encoder = rotaryio.IncrementalEncoder(board.D1, board.D2) # Rotary IO, change to suit the project
button_pins = [board.D0, board.D3, board.D6, board.D7, board.D8, board.D9, board.D10]

buttons = {}

redLed = digitalio.DigitalInOut(board.LED_RED)
redLed.direction = digitalio.Direction.OUTPUT

blueLed = digitalio.DigitalInOut(board.LED_BLUE)
blueLed.direction = digitalio.Direction.OUTPUT

greenLed = digitalio.DigitalInOut(board.LED_GREEN)
greenLed.direction = digitalio.Direction.OUTPUT

for pin in button_pins:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    # Add the button object to the dictionary with the pin name as the key
    buttons[pin] = button

print(f"Button map {buttons}")
# Now you can access the buttons using the pin names
# Example: Check if button D1 is pressed
# if not buttons[board.D1].value:
#    print("Button D1 is pressed")
