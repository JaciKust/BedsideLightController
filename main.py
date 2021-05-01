import json
import logging
import sys
import threading
import time
from datetime import datetime, timedelta

import zmq
from RPi import GPIO

from Interactable.ToggleableOnTimeCalculator import ToggleableOnTimeCalculator
from Sql.MarraQueryMaker import MarraQueryMaker

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

from Constants import Button as ButtonConstant
from Constants import DeskButton as DeskButtonConstant
from Constants import DoorButton as DoorButtonConstant
from Constants import MessageServer as MessageServerConstant
from Constants import PrimaryButton as PrimaryButtonConstant
from Constants import SecondaryButton as SecondaryButtonConstant
from DataObjects.DeskButtonColors import DeskButtonColor
from DataObjects.RemoteRelayState import RemoteRelayState
from DataObjects.Pulse import Pulse
from Interactable import Relays as RelayConstant
from PhysicalButton import PhysicalButton
from State.AwakeLightsOnState import AwakeLightsOnState


current_state = AwakeLightsOnState()
current_state.execute_state_change()

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def run_message_server():
    while True:
        #  Wait for next request from client
        message = incoming_socket.recv()
        incoming_socket.send(b"ack")
        logging.info("Received request: %s" % message)
        name, press_time = decode_button_press(message)
        set_new_state(current_state.get_state_for(name, press_time))

        sleep_time_seconds = 1
        time.sleep(sleep_time_seconds)


def send_to_desk_buttons(data):
    send(data, DeskButtonConstant.IP_ADDR, DeskButtonConstant.PORT, DeskButtonConstant.REQUEST_RETRIES,
         DeskButtonConstant.REQUEST_TIMEOUT)


def set_up_and_send_to_desk_buttons(right_colors, left_colors, rear_colors):
    right = list(map(lambda a: a.as_rgb_array(), right_colors))
    left = list(map(lambda a: a.as_rgb_array(), left_colors))
    rear = list(map(lambda a: a.as_rgb_array(), rear_colors))

    obj = DeskButtonColor(right, left, rear)
    data = json.dumps(obj.__dict__)
    send_to_desk_buttons(data)


def set_up_and_send_relay_change_to_desk_buttons(pin, is_on):
    obj = RemoteRelayState(pin, is_on)
    data = json.dumps(obj.__dict__)
    send_to_desk_buttons(data)


def set_up_and_send_pulse_relay_to_desk_buttons(pin):
    obj = Pulse(pin)
    data = json.dumps(obj.__dict__)
    send_to_desk_buttons(data)


def throw(pin, is_on):
    raise Exception('Cannot change state. Only pulse.')


RelayConstant.SOUND_SYSTEM_RELAY.send = set_up_and_send_relay_change_to_desk_buttons
RelayConstant.POWER_RELAY.pulse = set_up_and_send_pulse_relay_to_desk_buttons
RelayConstant.POWER_RELAY.send = throw


def send(data, ip_addr, port, request_retries, request_timeout):
    logging.info("Connecting to server…")
    client = context.socket(zmq.REQ)
    client.connect("tcp://{}:{}".format(ip_addr, port))

    request = str(data).encode()
    logging.info("Sending (%s)", request)
    client.send(request)

    retries_left = request_retries
    while True:
        if (client.poll(request_timeout) & zmq.POLLIN) != 0:
            reply = client.recv()
            if reply == b"ack":
                logging.info("Server replied OK (%s)", reply)
                break
            else:
                logging.error("Malformed reply from server: %s", reply)
                continue

        retries_left -= 1
        logging.warning("No response from server")
        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()
        if retries_left == 0:
            logging.error("Server seems to be offline, abandoning")
            return

        logging.info("Reconnecting to server…")
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect("tcp://{}:{}".format(ip_addr, port))
        logging.info("Resending (%s)", request)
        client.send(request)


def decode_button_press(message):
    parts = message.decode("utf-8").split('~')
    button_name = parts[0]
    button_press_time = float(parts[1])
    return button_name, button_press_time


context = zmq.Context()
incoming_socket = context.socket(zmq.REP)
incoming_socket.bind("tcp://{}:{}".format(MessageServerConstant.BIND_TO_ADDR, MessageServerConstant.BIND_TO_PORT))
socket_thread = threading.Thread(target=run_message_server)

primary_button = PhysicalButton(PrimaryButtonConstant.NAME,
                                PrimaryButtonConstant.RED_PWM,
                                PrimaryButtonConstant.GREEN_PWM,
                                PrimaryButtonConstant.BLUE_PWM,
                                PrimaryButtonConstant.TRIGGER_PIN)

secondary_button = PhysicalButton(SecondaryButtonConstant.NAME,
                                  SecondaryButtonConstant.RED_PWM,
                                  SecondaryButtonConstant.GREEN_PWM,
                                  SecondaryButtonConstant.BLUE_PWM,
                                  SecondaryButtonConstant.TRIGGER_PIN)

door_button = PhysicalButton(DoorButtonConstant.NAME,
                             DoorButtonConstant.RED_PWM,
                             DoorButtonConstant.GREEN_PWM,
                             DoorButtonConstant.BLUE_PWM,
                             DoorButtonConstant.TRIGGER_PIN)


def on_primary_button_press(channel):
    on_button_press(primary_button, current_state.get_primary_button_colors())


def on_door_button_press(channel):
    on_button_press(door_button, current_state.get_door_button_colors())


def on_secondary_button_press(channel):
    on_button_press(secondary_button, current_state.get_secondary_button_colors())


button_pressed = False


def on_button_press(button, colors):
    global button_pressed
    try:
        if button_pressed:
            return
        button_pressed = True
        global current_state
        button_start_press_time = time.time()
        button_press_time = 0
        has_long_press_been_set = False
        has_short_press_been_set = False
        time.sleep(0.01)

        while GPIO.input(button.trigger_pin) == ButtonConstant.BUTTON_PRESSED_VALUE and \
                button_press_time < ButtonConstant.EXTRA_LONG_PRESS_MIN:  # Wait for the button up

            button_press_time, has_long_press_been_set, has_short_press_been_set = \
                button.handle_button_color(button_start_press_time, has_long_press_been_set, has_short_press_been_set,
                                           colors)

        logging.info("{} Button pressed for {} seconds".format(button.name, round(button_press_time, 3)))
        set_new_state(current_state.get_state_for(button.name, button_press_time))
        wait_for_button_release(button.trigger_pin)

    except Exception:
        t, v, tb = sys.exc_info()
        logging.info("An error was encountered of type: {}".format(t))
        logging.info("Value: {}".format(v))
        logging.info(str(tb))
        raise
    finally:
        button_pressed = False


def set_new_state(state):
    global current_state
    if state is None:
        set_all_button_colors_to_default(current_state)
    else:
        old_state = current_state
        current_state = state
        logging.info("Setting state to: " + str(current_state))
        set_all_button_colors_to_default(current_state)

        old_state.execute_state_leave()
        current_state.execute_state_change()

        del old_state


def wait_for_button_release(channel):
    while GPIO.input(channel) == ButtonConstant.BUTTON_PRESSED_VALUE:
        time.sleep(0.1)


def init():
    logging.info('Starting')
    set_all_button_colors_to_default(current_state)

    GPIO.add_event_detect(primary_button.trigger_pin, GPIO.RISING, callback=on_primary_button_press,
                          bouncetime=ButtonConstant.BOUNCE_TIME_MS)

    GPIO.add_event_detect(secondary_button.trigger_pin, GPIO.RISING, callback=on_secondary_button_press,
                          bouncetime=ButtonConstant.BOUNCE_TIME_MS)

    GPIO.add_event_detect(door_button.trigger_pin, GPIO.RISING, callback=on_door_button_press,
                          bouncetime=ButtonConstant.BOUNCE_TIME_MS)

    socket_thread.start()


def set_all_button_colors_to_default(from_state):
    primary_button.set_button_color(from_state.get_primary_button_colors()[ButtonConstant.DEFAULT_COLOR])
    secondary_button.set_button_color(from_state.get_secondary_button_colors()[ButtonConstant.DEFAULT_COLOR])
    door_button.set_button_color(from_state.get_door_button_colors()[ButtonConstant.DEFAULT_COLOR])
    send_thread = threading.Thread(target=set_up_and_send_to_desk_buttons, args=(
        from_state.get_desk_right_button_colors(), from_state.get_desk_left_button_colors(),
        from_state.get_desk_rear_button_colors()))

    send_thread.start()


def get_time_in_toggleable_state(toggleable_id, state_to_time_in):
    marra = MarraQueryMaker.getInstance()
    marra.open_connection()
    initial = marra.get_latest_toggleable_state_for_yesterday(toggleable_id)

    initial.time_stamp = datetime(initial.time_stamp.year, initial.time_stamp.month, initial.time_stamp.day, 0,
                                  0) + timedelta(days=1)
    marra.close_connection()

    first = [initial]
    others = marra.get_time_stamps_for_toggleable_state_change_today(toggleable_id)
    if others is not None:
        first.extend(others)
    return ToggleableOnTimeCalculator.get_on_time(first, state_to_time_in)


if __name__ == '__main__':
    init()

    while True:
        time.sleep(10)
        try:
            new_state = current_state.on_time_expire_check()

            if new_state is not None:
                current_state = new_state
                current_state.execute_state_change()
                set_all_button_colors_to_default(current_state)

            time_on = get_time_in_toggleable_state(2, True)
            current_state.deal_with_light_time(time_on)

        except Exception as e:
            print("Throwing shit from loop.")
            t, v, tb = sys.exc_info()
            logging.error("An error was encountered of type: {}".format(t))
            logging.error("Value: {}".format(v))
            logging.error(str(tb))
            raise
