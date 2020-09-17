import sys
import time
from datetime import datetime

from RPi import GPIO

from Constants import Color as ColorConstant
from Constants import PrimaryButton as PrimaryButtonConstant
from State.AwakeLightsOnState import AwakeLightsOnState

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PrimaryButtonConstant.BLUE_PIN, GPIO.OUT)
GPIO.setup(PrimaryButtonConstant.RED_PIN, GPIO.OUT)
GPIO.setup(PrimaryButtonConstant.GREEN_PIN, GPIO.OUT)

LED_MAXIMUM = 100
blue_led = GPIO.PWM(PrimaryButtonConstant.BLUE_PIN, LED_MAXIMUM)
red_led = GPIO.PWM(PrimaryButtonConstant.RED_PIN, LED_MAXIMUM)
green_led = GPIO.PWM(PrimaryButtonConstant.GREEN_PIN, LED_MAXIMUM)

previous_color = None
current_state = AwakeLightsOnState()
current_state.execute_state_change()


def log_data(data):
    now = str(datetime.now())
    data = str(data)
    output = '[{}] {}'.format(now, data)
    print(output)


def set_button_color(color):
    global previous_color
    if previous_color == color:
        return
    previous_color = color
    red_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.RED_LOCATION])
    green_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.GREEN_LOCATION])
    blue_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.BLUE_LOCATION])


def on_button_press(channel):
    try:
        global current_state
        button_start_press_time = time.time()
        button_press_time = 0
        has_long_press_been_set = False
        has_short_press_been_set = False
        time.sleep(0.01)

        while GPIO.input(channel) == PrimaryButtonConstant.BUTTON_PRESSED_VALUE and \
                button_press_time < PrimaryButtonConstant.EXTRA_LONG_PRESS_MIN:  # Wait for the button up
            button_press_time, has_long_press_been_set, has_short_press_been_set = \
                handle_button_color(button_start_press_time, has_long_press_been_set, has_short_press_been_set)

        log_data("Button pressed for {} seconds".format(round(button_press_time, 3)))
        set_new_state(get_new_state(button_press_time))
        wait_for_button_release(channel)

    except Exception:
        type, value, traceback = sys.exc_info()
        log_data("An error was encountered of type: {}".format(type))
        log_data("Value: {}".format(value))
        log_data(str(traceback))
        raise


def set_new_state(state):
    global current_state
    if state is None:
        set_button_color(current_state.ring_color)
    else:
        current_state = state
        log_data("Setting state to: " + str(current_state))
        set_button_color(current_state.ring_color)
        current_state.execute_state_change()


def wait_for_button_release(channel):
    while GPIO.input(channel) == PrimaryButtonConstant.BUTTON_PRESSED_VALUE:
        time.sleep(0.1)


def get_new_state(button_time):
    return_state = None
    # extra long press
    if button_time >= PrimaryButtonConstant.EXTRA_LONG_PRESS_MIN:
        return_state = current_state.on_extra_long_press()
    # long button press
    elif button_time >= PrimaryButtonConstant.LONG_PRESS_MIN:
        return_state = current_state.on_long_press()
    # short press
    elif button_time >= PrimaryButtonConstant.NOISE_THRESHOLD:
        return_state = current_state.on_short_press()
    return return_state


def handle_button_color(button_start_press_time, has_long_press_been_set, has_short_press_been_set):
    button_press_time = time.time() - button_start_press_time
    if not has_long_press_been_set and button_press_time >= PrimaryButtonConstant.LONG_PRESS_MIN:
        has_long_press_been_set = True
        set_button_color(current_state.on_long_press_ring_color)
    elif not has_short_press_been_set:
        has_short_press_been_set = True
        set_button_color(current_state.on_press_ring_color)
    time.sleep(0.1)
    return button_press_time, has_long_press_been_set, has_short_press_been_set


def on_start():
    log_data('Starting')
    red_led.start(100)
    green_led.start(100)
    blue_led.start(100)
    set_button_color(current_state.ring_color)
    GPIO.setup(PrimaryButtonConstant.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(PrimaryButtonConstant.TRIGGER_PIN, GPIO.RISING, callback=on_button_press,
                          bouncetime=PrimaryButtonConstant.BOUNCE_TIME_MS)


if __name__ == '__main__':
    on_start()

    while True:
        time.sleep(60)
        new_state = current_state.on_time_expire_check()

        if new_state is not None:
            current_state = new_state
            current_state.execute_state_change()
            set_button_color(current_state.ring_color)
