from datetime import datetime
from RPi import GPIO
import time
from State.AwakeLightsOnState import AwakeLightsOnState
from Constants import Color as ColorConstant
from Constants import PrimaryButton as PrimaryButtonConstant

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


def set_button_color(color):
    global previous_color
    if previous_color == color:
        return
    previous_color = color
    red_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.RED_LOCATION])
    green_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.GREEN_LOCATION])
    blue_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.BLUE_LOCATION])


def on_button_press(channel):
    global current_state
    start_time = time.time()
    button_time = 0
    has_long_press_been_set = False
    has_short_press_been_set = False
    time.sleep(0.01)

    while GPIO.input(channel) == PrimaryButtonConstant.BUTTON_PRESSED_VALUE and \
            button_time < PrimaryButtonConstant.EXTRA_LONG_PRESS_MIN:  # Wait for the button up
        button_time, has_long_press_been_set, has_short_press_been_set = \
            handle_button_color(start_time, has_long_press_been_set, has_short_press_been_set)

    set_new_state(get_new_state(button_time))
    wait_for_button_release(channel)


def set_new_state(state):
    global current_state
    if state is None:
        set_button_color(current_state.get_ring_color())
    else:
        current_state = state
        set_button_color(current_state.get_ring_color())
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


def handle_button_color(start_time, has_long_press_been_set, has_short_press_been_set):
    button_time = time.time() - start_time
    if not has_long_press_been_set and button_time >= PrimaryButtonConstant.LONG_PRESS_MIN:
        has_long_press_been_set = True
        set_button_color(current_state.get_ring_color_on_long_press())
    elif not has_short_press_been_set:
        has_short_press_been_set = True
        set_button_color(current_state.get_ring_color_on_press())
    time.sleep(0.1)
    return button_time, has_long_press_been_set, has_short_press_been_set


if __name__ == '__main__':
    red_led.start(100)
    green_led.start(100)
    blue_led.start(100)
    set_button_color(current_state.get_ring_color())

    GPIO.setup(PrimaryButtonConstant.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(PrimaryButtonConstant.TRIGGER_PIN, GPIO.RISING, callback=on_button_press, bouncetime=PrimaryButtonConstant.BOUNCE_TIME_MS)
    print("Current time: " + str(datetime.now()))

    while True:
        time.sleep(20)
        print('checking from while')
        new_state = current_state.on_time_expire_check()

        if new_state is not None:
            print("Executing state change based on time")
            current_state = new_state
            current_state.execute_state_change()
            set_button_color(current_state.get_ring_color())
