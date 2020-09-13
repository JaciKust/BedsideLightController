from datetime import datetime
from RPi import GPIO
import time
from State.AwakeLightsOnState import AwakeLightsOnState
from Constants import Color as ColorConstant, PrimaryButton

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Ignore warning for now

GPIO.setup(PrimaryButton.BLUE_PIN, GPIO.OUT)
GPIO.setup(PrimaryButton.RED_PIN, GPIO.OUT)
GPIO.setup(PrimaryButton.GREEN_PIN, GPIO.OUT)

LED_MAXIMUM = 100
blue_led = GPIO.PWM(PrimaryButton.BLUE_PIN, LED_MAXIMUM)
red_led = GPIO.PWM(PrimaryButton.RED_PIN, LED_MAXIMUM)
green_led = GPIO.PWM(PrimaryButton.GREEN_PIN, LED_MAXIMUM)
previous_color = None


def set_led_color(color):
    global previous_color
    if previous_color == color:
        return
    previous_color = color
    print("Setting color to: " + str(color))
    red_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.RED_LOCATION])
    green_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.GREEN_LOCATION])
    blue_led.ChangeDutyCycle(LED_MAXIMUM - color[ColorConstant.BLUE_LOCATION])


current_state = AwakeLightsOnState()
current_state.execute_state_change()


def button_callback(channel):
    global current_state
    start_time = time.time()
    button_time = 0
    time.sleep(0.01)
    print('button pressed')
    while GPIO.input(channel) == PrimaryButton.BUTTON_PRESSED_VALUE and button_time < PrimaryButton.EXTRA_LONG_PRESS_MIN:  # Wait for the button up
        print("In button loop")
        button_time = time.time() - start_time
        set_long_press = False
        set_press = False
        if not set_long_press and button_time >= PrimaryButton.LONG_PRESS_MIN:
            set_long_press = True
            set_led_color(current_state.get_ring_color_on_long_press())
        elif not set_press:
            set_press = True
            set_led_color(current_state.get_ring_color_on_press())
        time.sleep(0.1)

    print('continuing')

    is_noise_press = False

    new_state = None
    # extra long press
    if button_time >= PrimaryButton.EXTRA_LONG_PRESS_MIN:
        new_state = current_state.on_extra_long_press()
    # long button press
    elif button_time >= PrimaryButton.LONG_PRESS_MIN:
        new_state = current_state.on_long_press()
    # short press
    elif button_time >= PrimaryButton.NOISE_THRESHOLD:
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
        while GPIO.input(channel) == PrimaryButton.BUTTON_PRESSED_VALUE:
            time.sleep(0.1)

        print("Press time: " + str(button_time))


if __name__ == '__main__':
    red_led.start(100)
    green_led.start(100)
    blue_led.start(100)
    set_led_color(current_state.get_ring_color())

    GPIO.setup(PrimaryButton.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(PrimaryButton.TRIGGER_PIN, GPIO.RISING, callback=button_callback, bouncetime=PrimaryButton.BOUNCE_TIME_MS)
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
