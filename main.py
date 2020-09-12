from datetime import datetime

from RPi import GPIO
import time

import Lights
from AwakeLightsOnState import AwakeLightsOnState
import ColorConstants
import colorsys
from lifxlan import Light

import PrimaryButtonConstants


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Ignore warning for now

GPIO.setup(PrimaryButtonConstants.BLUE_PIN, GPIO.OUT)
GPIO.setup(PrimaryButtonConstants.RED_PIN, GPIO.OUT)
GPIO.setup(PrimaryButtonConstants.GREEN_PIN, GPIO.OUT)

LED_MAXIMUM = 100
blue_led = GPIO.PWM(PrimaryButtonConstants.BLUE_PIN, LED_MAXIMUM)
red_led = GPIO.PWM(PrimaryButtonConstants.RED_PIN, LED_MAXIMUM)
green_led = GPIO.PWM(PrimaryButtonConstants.GREEN_PIN, LED_MAXIMUM)

def set_led_color(color):
    red_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstants.RED_LOCATION])
    green_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstants.GREEN_LOCATION])
    blue_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstants.BLUE_LOCATION])


current_state = AwakeLightsOnState()
current_state.execute_state_change()


def button_callback(channel):
    global current_state
    start_time = time.time()
    button_time = 0
    set_led_color(current_state.get_ring_color_on_press())
    print('button pressed')
    while GPIO.input(channel) == PrimaryButtonConstants.BUTTON_PRESSED_VALUE and button_time < PrimaryButtonConstants.EXTRA_LONG_PRESS_MIN:  # Wait for the button up
        time.sleep(0.1)
        button_time = time.time() - start_time
        if button_time >= PrimaryButtonConstants.LONG_PRESS_MIN:
            set_led_color(current_state.get_ring_color_on_long_press())

    print('continuing')

    is_noise_press = False

    new_state = None
    # extra long press
    if button_time >= PrimaryButtonConstants.EXTRA_LONG_PRESS_MIN:
        new_state = current_state.on_extra_long_press()
    # long button press
    elif button_time >= PrimaryButtonConstants.LONG_PRESS_MIN:
        new_state = current_state.on_long_press()
    # short press
    elif button_time >= PrimaryButtonConstants.NOISE_THRESHOLD:
        new_state = current_state.on_short_press()
    # noise
    else:
        print("Was determined to be noise")
        is_noise_press = True

    if new_state is None:
        print("-----------> No state change detected.")
        set_led_color(current_state.get_ring_color())
    else:
        current_state = new_state
        set_led_color(current_state.get_ring_color())
        current_state.execute_state_change()

    if not is_noise_press:
        # Wait for button to be released if still pressed for extra long press.
        while GPIO.input(channel) == PrimaryButtonConstants.BUTTON_PRESSED_VALUE:
            time.sleep(0.1)

        print("Press time: " + str(button_time))


if __name__ == '__main__':
    red_led.start(100)
    green_led.start(100)
    blue_led.start(100)
    set_led_color(current_state.get_ring_color())

    GPIO.setup(PrimaryButtonConstants.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(PrimaryButtonConstants.TRIGGER_PIN, GPIO.RISING, callback=button_callback, bouncetime=PrimaryButtonConstants.BOUNCE_TIME)
    print("Current time: " + str(datetime.now()))

    while True:
        time.sleep(20)
        print('checking from while')
        new_state = current_state.on_time_expire_check()

        if new_state is not None:
            print("Executing state change based on time")
            current_state = new_state
            current_state.execute_state_change()
            set_led_color(current_state.get_ring_color())
