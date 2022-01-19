# John Nooney - 1803534
# This script will allow for control of the button and LEDs
# when the button is pressed it will generate a session log to send to DynamoDB
# and it will also start up the AirPlay Server. If the button is clicked again
# another log will be sent and the AirPlay server will be killed.

import json
import datetime
import subprocess as sp
import boto3
import time
from gpiozero import LED
from gpiozero import Button
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

    # put item as specificed json format
    def generate_log(self):
        time_delta = datetime.datetime.now() - self.start_time
        user = "tester1"
        data_str = '{"RpiDateTime":"00:00:0123","RpiUser":"'+user+'\
        ","RpiSession":"'+str(self.counter)+'\
        ","RpiSessionStatus": "active",\
        "RpiDuration":"00:00:0123","RpiFault": "none",\
        "RpiRestarts":"'+str(self.restarts)+'"}'

        data_json = json.loads(data_str)
        data_json["RpiDateTime"] = str(self.start_time)
        data_json["RpiDuration"] = str(time_delta)
        return data_json

    def handle(self):
        print("button press")
        self.state = not self.state
        self.counter+=1
        table = self.dynamo_get_table(self.table_name)

        if self.state:

            # turn on green LED
            print("Green LED on.")
            self.green_led.on()
            self.red_led.off()

            # construct log
            print("Sending initial log to AWS...")
            data = self.generate_log()
            print("generated log: ", data)
            # send log to aws
            self.dynamo_put(table, data)

            # blink led
            self.green_led.off()
            time.sleep(.5)
            self.green_led.on()

            
            # start AirPlay server as background process
            print("Starting AirPlay Server...")
            sp.Popen("/home/pi/Downloads/RPiPlay/build/rpiplay", shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            print("Check your IPhone for RPiPlay in the AirPlay menu.")
            print("To turn off AirPlay Server press the button again.")
        else:
            # turn on red LED
            print("Red LED on.")
            self.green_led.off()
            self.red_led.on()

            # stop airplay server
            print("Stopping AirPlay Server...")
            cmd = "pkill -f rpiplay"
            sp.run(["pkill","-f","rpiplay"])
            print("AirPlay server stopped.")

            # construct log
            print("Sending concluding log to AWS...")
            data = self.generate_log()
            print("generated log: ", data)
            # submit log
            self.dynamo_put(table, data)

            print("To start the AirPlay server again press the button.")
            self.restarts+=1

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
    def dynamo_put(self, table, data):
        request = table.put_item(Item=data)
        print(request)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Welcome to the RPi and AWS controller!")
    print("press your button to start the AirPlay server")
    flag = True
    rpi = RpiHandler("rpi-aws-log")

    while(flag):
        rpi.button.when_pressed = rpi.handle

