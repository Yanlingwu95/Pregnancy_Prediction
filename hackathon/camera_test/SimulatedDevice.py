# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import math
from grove.adc import ADC
from Adafruit_BME280 import *

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# Sensor
class GroveLightSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value

class GroveMoistureSensor:

    def __init__(self, channe2):
        self.channe2 = channe2
        self.adc = ADC()

    @property
    def mositure(self):
        value = self.adc.read(self.channe2)
        return value

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=myhob.azure-devices.net;DeviceId=ippot;SharedAccessKey=sk9RyGmtPUXHEqbV00PSG0F8oNTfNaZVJJ9XiTdYri4="
# CONNECTION_STRING = "HostName=CC-project-hub.azure-devices.net;DeviceId=Raspberry-Pi;SharedAccessKey=L0roOnzlbkhvu3O6GSKWMMcwTTu06Rh2IKeQingYXzs="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
MSG_TXT = "{\"Time\": %s,\"Temp\": %.2f,\"Pressure\": %.2f,\"Humidity\": %.2f,\"Light\": %d,\"Moisture\": %d}"

light_pin = 2
moisture_pin = 0

light_sensor = GroveLightSensor(light_pin)
moisture_sensor = GroveMoistureSensor(moisture_pin)

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

# Handle direct method calls from IoT Hub
def device_method_callback(method_name, payload, user_context):
    global INTERVAL
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s" % (method_name, payload) )
    # print ("Hello World\n")
    device_method_return_value = DeviceMethodReturnValue()
    methods = method_name.split()
    response = ""
    error = False
    
    if methods[0] == "Tup":
        print("Temperature up")
        response += "Temperature up, "
    elif methods[0] == "Tdown":
        print("Temperature down")
        response += "Temperature down"
    elif methods[0] == "Tst":
        print("Temperature stay")
        response += "Temperature stay"
    else:
        print("Error! Temperature method name is wrong!")
        error = True
        
    if methods[1] == "Hup":
        print("Humidity up")
        response += "Humidity up, "
    elif methods[1] == "Hdown":
        print("Humidity down")
        response += "Humidity down, "
    elif methods[1] == "Hst":
        print("Humidity stay")
        response += "Humidity stay, "
    else:
        print("Error! Humidity method name is wrong!")
        error = True
        
    if methods[2] == "Mup":
        print("Moisture up")
        response += "Moisture up, "
    elif methods[2] == "Mdown":
        print("Moisture down")
        response += "Moisture down, "
    elif methods[2] == "Mst":
        print("Moisture stay")
        response += "Moisture stay, "
    else:
        print("Error! Moisture method name is wrong!")
        error = True
        
    if methods[3] == "Lup":
        print("Light up")
        response += "Light up. "
    elif methods[3] == "Ldown":
        print("Light down")
        response += "Light down, "
    elif methods[3] == "Lst":
        print("Light stay")
        response += "Light stay, "
    else:
        print("Error! Light method name is wrong!")
        error = True
    
    if error == False:
        # Build and send an error response.
        device_method_return_value.response = "{ \"Response\": \"Executed direct method %s\" }" % response
        device_method_return_value.status = 200
    else:
        device_method_return_value.response = "{ \"Response\": \"Invalid parameter\" }"
        device_method_return_value.status = 400

    return device_method_return_value

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Set up the callback method for direct method calls from the hub.
        client.set_device_method_callback(
            device_method_callback, None)

        while True:
            time_c = time.ctime() 
            Time = "\"" + str(time_c) + "\""
            BMEsensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

            degrees = BMEsensor.read_temperature()
            pascals = BMEsensor.read_pressure()
            hectopascals = pascals / 100
            humidity = BMEsensor.read_humidity()
            
            # Build the message with simulated telemetry values.
            msg_txt_formatted = MSG_TXT % (Time, degrees, hectopascals, humidity, light_sensor.light, moisture_sensor.mositure)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if degrees > 30:
              prop_map.add("temperatureAlert", "true")
            else:
              prop_map.add("temperatureAlert", "false")

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
