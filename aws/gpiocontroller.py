import json
import datetime
import subprocess
import boto3
import time
from gpiozero import LED
from gpiozero import Button
# import RPi.GPIO as GPIO
# Red led = gpio 24
# Green led = gpio 18
# Button = gpio 3

class RpiHandler:
    def __init__(self, table_name):
        self.state = False
        self.start_time = datetime.datetime.now()
        self.green_led = LED(18)
        self.red_led = LED(24)
        self.button = Button(3)
        self.counter = 0
        self.restarts = 0
        self.table_name = table_name

    def start_subprocess(self, cmd):
        output = subprocess.run(cmd, capture_output=True)
        print(output)

    # put item as specificed json format
    def generate_log(self):
        time_delta = str(datetime.datetime.now() - self.start_time)
        user = "tester1"
        data_str = '{"RpiDateTime":"'+self.start_time+'\
        ","RpiUser":"'+user+'\
        ","RpiSession":"'+self.counter+'\
        ","RpiSessionStatus": "active",\
        "RpiDuration":"00:00:0123","RpiFaults": "none",\
        "RpiRestarts":"'+self.restarts+'"}'

        data_json = json.load(data_str)
        data_json["RpiDuration"] = time_delta
        return data_json

    def handle(self):
        print("button press")
        self.state = not self.state
        self.counter+=1
        table = self.dynamo_get_table(self.table_name)

        if self.state:

            # turn on green LED
            self.green_led.on()
            self.red_led.off()

            # construct log
            data = self.generate_log()
            print("generated log: ", data)
            # send log to aws
            self.dynamo_put(table, data)

            # blink led
            self.green_led.off()
            time.sleep(.5)
            self.green_led.on()

            
            # start AirPlay server
            cmd = "/home/pi/Downloads/RpiPlay/build/rpiplay"
            self.start_subprocess(cmd)
        else:
            # turn on red LED
            self.green_led.off()
            self.red_led.on()

            # stop airplay server
            cmd = "pkill -f rpiplay"
            self.start_subprocess(cmd)

            # construct log
            data = self.generate_log()
            print("generated log: ", data)
            # submit log
            self.dynamo_put(table, data)

    def dynamo_get_table(self, name):
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

        # Instantiate a table resource object without actually
        # creating a DynamoDB table. Note that the attributes of this table
        # are lazy-loaded: a request is not made nor are the attribute
        # values populated until the attributes
        # on the table resource are accessed or its load() method is called.
        table = dynamodb.Table(name)

        # Print out some data about the table.
        # This will cause a request to be made to DynamoDB and its attribute
        # values will be set based on the response.
        print(table.creation_date_time)
        return table

    # put item as specificed json format
    def dynamo_put(self, data):
        request = self.table.put_item(Item=data)
        print(request)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    flag = True
    rpi = RpiHandler("rpi-aws-log")

    while(flag):
        rpi.button.when_pressed = rpi.handle

