import sys
import time
from datetime import datetime

from RPi import GPIO

from Constants import Button as ButtonConstant
from Constants import DoorButton as DoorButtonConstant
from Constants import PrimaryButton as PrimaryButtonConstant
from Constants import SecondaryButton as SecondaryButtonConstant
from PhysicalButton import PhysicalButton
from State.AwakeLightsOnState import AwakeLightsOnState

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

current_state = AwakeLightsOnState()
current_state.execute_state_change()

primary_button = PhysicalButton(PrimaryButtonConstant.NAME,
                                PrimaryButtonConstant.RED_PIN,
                                PrimaryButtonConstant.GREEN_PIN,
                                PrimaryButtonConstant.BLUE_PIN,
                                PrimaryButtonConstant.TRIGGER_PIN)

secondary_button = PhysicalButton(SecondaryButtonConstant.NAME,
                                  SecondaryButtonConstant.RED_PIN,
                                  SecondaryButtonConstant.GREEN_PIN,
                                  SecondaryButtonConstant.BLUE_PIN,
                                  SecondaryButtonConstant.TRIGGER_PIN)

door_button = PhysicalButton(DoorButtonConstant.NAME,
                             DoorButtonConstant.RED_PIN,
                             DoorButtonConstant.GREEN_PIN,
                             DoorButtonConstant.BLUE_PIN,
                             DoorButtonConstant.TRIGGER_PIN)


def log_data(data):
    now = str(datetime.now())
    data = str(data)
    output = '[{}] {}'.format(now, data)
    print(output)


def on_primary_button_press(channel):
    try:
        global current_state
        button_start_press_time = time.time()
        button_press_time = 0
        has_long_press_been_set = False
        has_short_press_been_set = False
        time.sleep(0.01)

        while GPIO.input(channel) == ButtonConstant.BUTTON_PRESSED_VALUE and \
                button_press_time < ButtonConstant.EXTRA_LONG_PRESS_MIN:  # Wait for the button up

            button_press_time, has_long_press_been_set, has_short_press_been_set = \
                primary_button.handle_button_color(button_start_press_time, has_long_press_been_set,
                                                   has_short_press_been_set, current_state.get_primary_button_colors())

        log_data("Primary Button pressed for {} seconds".format(round(button_press_time, 3)))
        set_new_state(primary_button.get_new_state_from_press(current_state, button_press_time))
        wait_for_button_release(channel)

    except Exception:
        t, v, tb = sys.exc_info()
        log_data("An error was encountered of type: {}".format(t))
        log_data("Value: {}".format(v))
        log_data(str(tb))
        raise


def set_new_state(state):
    global current_state
    if state is None:
        primary_button.set_button_color(current_state.get_primary_button_colors()[ButtonConstant.DEFAULT_COLOR])
    else:
        print("Throwing shit from set state")
        current_state = state
        log_data("Setting state to: " + str(current_state))
        primary_button.set_button_color(current_state.get_primary_button_colors()[ButtonConstant.DEFAULT_COLOR])
        current_state.execute_state_change()


def wait_for_button_release(channel):
    while GPIO.input(channel) == ButtonConstant.BUTTON_PRESSED_VALUE:
        time.sleep(0.1)

def init():
    log_data('Starting')
    primary_button.set_button_color(current_state.get_primary_button_colors()[ButtonConstant.DEFAULT_COLOR])

    GPIO.add_event_detect(primary_button.trigger_pin, GPIO.RISING, callback=on_primary_button_press,
                          bouncetime=ButtonConstant.BOUNCE_TIME_MS)

    GPIO.add_event_detect(secondary_button.trigger_pin, GPIO.RISING, callback=on_primary_button_press,
                          bouncetime=ButtonConstant.BOUNCE_TIME_MS)

    GPIO.add_event_detect(door_button.trigger_pin, GPIO.RISING, callback=on_primary_button_press,
                          bouncetime=ButtonConstant.BOUNCE_TIME_MS)


if __name__ == '__main__':
    init()

    while True:
        time.sleep(60)
        try:
            new_state = current_state.on_time_expire_check()

            if new_state is not None:
                current_state = new_state
                current_state.execute_state_change()
                primary_button.set_button_color(current_state.get_primary_button_colors()[ButtonConstant.DEFAULT_COLOR])

        except:
            print("Throwing shit from loop.")
            t, v, tb = sys.exc_info()
            log_data("An error was encountered of type: {}".format(t))
            log_data("Value: {}".format(v))
            log_data(str(tb))
            raise
