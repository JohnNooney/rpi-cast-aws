import json
import datetime
import subprocess
from gpiozero import LED
from gpiozero import Button

# Red led = gpio 24
# Green led = gpio 18
# Button = gpio 3


def start_subprocess(cmd):
    output = subprocess.run(cmd, capture_output=True)
    print(output)

# put item as specificed json format
def generate_log(table, data):
    request = table.put_item(Item=data)
    print(request)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    state = False
    flag = True
    start_time = datetime.datetime.now()
    green_led = LED(18)
    red_led = LED(24)
    button = Button(3)
    counter = 0

    while(flag):
        button.wait_for_press()
        counter+=1
        state != state

        print("times pressed:", counter)

        if state:
            # turn on green LED
            green_led.on()
            red_led.off()

            # construct log
            # send log to aws
            # start AirPlay server
        else:
            # turn on red LED
            green_led.off()
            red_led.on()

            # stop airplay server
            # construct log
            # submit log

    print(data)

    dynamo_put(table, data)
