import logging

import Color as ColorConstant
from Constants import Button as ButtonConstant
from Constants import DeskButton as DeskButtonConstant
from Constants import DoorButton as DoorButtonConstant
from Constants import PrimaryButton as PrimaryButtonConstant
from Constants import Relay as RelayConstant
from Constants import SecondaryButton as SecondaryButtonConstant
from Interactable.Relay import Relay
from Sql.MarraQueryMaker import MarraQueryMaker
from Transmitter433 import Transmitter433


class State:
    name = 'Base State'
    id = -1

    def __init__(self, previous_state):
        self.previous_state = previous_state

        transmitter433 = Transmitter433()
        self.fan = transmitter433.fan
        self.monitor = transmitter433.monitor
        self.plant_lights = transmitter433.plant_lights
        self.oddish_light = Relay(RelayConstant.ID, RelayConstant.ODDISH_RELAY_PIN)

        self.maker = MarraQueryMaker.getInstance()
        self.maker.open_connection()
        if previous_state is None or previous_state.current_white is None:
            self.current_white = ColorConstant.WHITES_IN_KELVIN_CYCLE[ColorConstant.WHITE_START_INDEX]
        else:
            self.current_white = previous_state.current_white

    def execute_state_change(self):
        print("State changed to " + self.name)
        self._update_database()

    def _update_database(self):
        try:
            self.maker.insert_state_status(self.id)
        except:
            print("Unable to update database state for " + str(self.id))
            pass

    # region Button Color

    def get_primary_button_colors(self):
        raise NotImplemented('Getting the primary button color is not implemented for class ' + self.name)

    def get_secondary_button_colors(self):
        return [ColorConstant.DIM_BLUE, ColorConstant.BLUE, ColorConstant.RED]

    def get_door_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]

    # endregion

    # region Button Actions

    def get_desk_right_button_colors(self):
        return self.get_secondary_button_colors()

    def get_desk_left_button_colors(self):
        return self.get_primary_button_colors()

    def get_desk_rear_button_colors(self):
        return [ColorConstant.DIM_GREEN, ColorConstant.GREEN, ColorConstant.RED]

    def on_primary_short_press(self):
        return None

    def on_primary_long_press(self):
        return None

    def on_primary_extra_long_press(self):
        return None

    def on_secondary_short_press(self):
        self.fan.toggle()
        return None

    def on_secondary_long_press(self):
        self.plant_lights.toggle()
        if self.plant_lights.get_is_on():
            self.oddish_light.set_on()
        else:
            self.oddish_light.set_off()
        return None

    def on_secondary_extra_long_press(self):
        self.monitor.toggle()
        return None

    def on_door_short_press(self):
        return None

    def on_door_long_press(self):
        return None

    def on_door_extra_long_press(self):
        return None

    def on_desk_right_short_press(self):
        return self.on_secondary_short_press()

    def on_desk_right_long_press(self):
        return self.on_secondary_long_press()

    def on_desk_right_extra_long_press(self):
        return self.on_secondary_extra_long_press()

    def on_desk_left_short_press(self):
        return self.on_primary_short_press()

    def on_desk_left_long_press(self):
        return self.on_primary_long_press()

    def on_desk_left_extra_long_press(self):
        return self.on_primary_extra_long_press()

    def on_desk_rear_short_press(self):
        self.cycle_kelvin()

    def on_desk_rear_long_press(self):
        return None

    def on_desk_rear_extra_long_press(self):
        return None

    # endregion

    # region Light Kelvin Change

    current_white = None

    def on_kelvin_changed(self):
        pass

    def cycle_kelvin(self):
        try:
            location = ColorConstant.WHITES_IN_KELVIN_CYCLE.index(self.current_white)
        except:
            location = -1
        location += 1
        location %= len(ColorConstant.WHITES_IN_KELVIN_CYCLE)
        self.current_white = ColorConstant.WHITES_IN_KELVIN_CYCLE[location]
        self.on_kelvin_changed()

    def set_default_white(self):
        pass

    # endregion

    # region Get State for Button

    def get_state_for(self, button_name, press_time):
        if button_name == PrimaryButtonConstant.NAME:
            return self.get_state_for_primary_button(press_time)

        if button_name == SecondaryButtonConstant.NAME:
            return self.get_state_for_secondary_button(press_time)

        if button_name == DoorButtonConstant.NAME:
            return self.get_state_for_door_button(press_time)

        if button_name == DeskButtonConstant.RIGHT:
            return self.get_state_for_desk_right(press_time)

        if button_name == DeskButtonConstant.LEFT:
            return self.get_state_for_desk_left(press_time)

        if button_name == DeskButtonConstant.REAR:
            return self.get_state_for_desk_rear(press_time)

        logging.error("Could not determine button name.")

    def get_state_for_primary_button(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_primary_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_primary_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_primary_short_press()
        return return_state

    def get_state_for_secondary_button(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_secondary_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_secondary_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_secondary_short_press()
        return return_state

    def get_state_for_door_button(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_door_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_door_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_door_short_press()
        return return_state

    def get_state_for_desk_right(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_desk_right_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_desk_right_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_desk_right_short_press()
        return return_state

    def get_state_for_desk_left(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_desk_left_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_desk_left_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_desk_left_short_press()
        return return_state

    def get_state_for_desk_rear(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_desk_rear_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_desk_rear_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_desk_rear_short_press()

        return return_state

    # endregion

    # region Time

    def on_time_expire_check(self):
        return None

    # endregion

    def __eq__(self, other):
        return other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name
