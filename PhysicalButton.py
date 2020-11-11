import time
from datetime import datetime

from RPi import GPIO

from Constants import Button as ButtonConstant
from Constants import Color as ColorConstant


class PhysicalButton:
    current_color = None
    previous_color = None
    LED_MAXIMUM = 100

    def __init__(self, name, red_led_pin, green_led_pin, blue_led_pin, trigger_pin):
        GPIO.setup(red_led_pin, GPIO.OUT)
        GPIO.setup(green_led_pin, GPIO.OUT)
        GPIO.setup(blue_led_pin, GPIO.OUT)
        GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.name = name

        self.red_led = GPIO.PWM(red_led_pin, self.LED_MAXIMUM)
        self.green_led = GPIO.PWM(green_led_pin, self.LED_MAXIMUM)
        self.blue_led = GPIO.PWM(blue_led_pin, self.LED_MAXIMUM)

        self.red_led.start(100)
        self.green_led.start(100)
        self.blue_led.start(100)

        self.trigger_pin = trigger_pin
        pass

    def set_button_color(self, color):
        if self.previous_color == color:
            return
        self.previous_color = color
        self.red_led.ChangeDutyCycle(self.LED_MAXIMUM - color[ColorConstant.RED_LOCATION])
        self.green_led.ChangeDutyCycle(self.LED_MAXIMUM - color[ColorConstant.GREEN_LOCATION])
        self.blue_led.ChangeDutyCycle(self.LED_MAXIMUM - color[ColorConstant.BLUE_LOCATION])

    def handle_button_color(self, button_start_press_time, has_long_press_been_set, has_short_press_been_set,
                            button_colors):
        button_press_time = time.time() - button_start_press_time
        if not has_long_press_been_set and button_press_time >= ButtonConstant.LONG_PRESS_MIN:
            has_long_press_been_set = True
            self.set_button_color(button_colors[ButtonConstant.LONG_PRESS_COLOR_LOCATION])
        elif not has_short_press_been_set:
            has_short_press_been_set = True
            self.set_button_color(button_colors[ButtonConstant.PRESS_COLOR_LOCATION])
        time.sleep(0.1)
        return button_press_time, has_long_press_been_set, has_short_press_been_set

    def log_data(self, data):
        now = str(datetime.now())
        data = str(data)
        output = '[{}] {}'.format(now, data)
        print(output)
