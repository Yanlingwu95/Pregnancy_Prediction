# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import math
# from grove.adc import ADC
# from Adafruit_BME280 import *
import os
import threading as th
import multiprocessing 
from multiprocessing import pool
from multiprocessing import Process
import pandas as pd
import numpy as np
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

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
CONNECTION_STRING = "HostName=Trail413.azure-devices.net;DeviceId=mynewdevice;SharedAccessKey=NYoyx/ib9kq1og6eDwIRXgwd4zCQmEnINLGtrSoUAdk="
# CONNECTION_STRING = "HostName=CC-project-hub.azure-devices.net;DeviceId=Raspberry-Pi;SharedAccessKey=L0roOnzlbkhvu3O6GSKWMMcwTTu06Rh2IKeQingYXzs="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
#Read data from file 
# MSG_TXT = "{\"Time\": %s,\"Temp\": %.2f,\"Pressure\": %.2f,\"Humidity\": %.2f,\"Light\": %d,\"Moisture\": %d}"
data = pd.read_csv('./row_data.csv')
columns = data.columns
MSG_TXT ="{"
for i in range(len(columns)):
    if i == len(columns) - 1:
        MSG_TXT += "\""+columns[i]+"\": %.2f"
    else:
        MSG_TXT += "\""+columns[i]+"\": %.2f,"
MSG_TXT += "}"

# light_sensor = GroveLightSensor(light_pin)
# moisture_sensor = GroveMoistureSensor(moisture_pin)

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
    ## Upload file to blob on Azure
    if method_name == "send_file":
        filename = 'firstdata'+payload+'.json'
        block_blob_service = BlockBlobService(account_name='cs2743a315b9ea3x49fdxb30', account_key='fiGff9v/aulWyb6T3eUupbS4hS2ygfwmTmAQ55+xA+q+enpqIJfaPRfqSQ9paP2idEoj+FYaU7wX+FWWHfSkPQ==')
        block_blob_service.create_blob_from_path(
                            'mydata', #blob name
                            filename, #blob's file name
                            'row_data.json', # local file name
                            content_settings=ContentSettings(content_type='json'))
        response = 'OK'
        error = False

    else:
        response = 'Fail'
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

        for i in range(data.shape[0]):
            time_c = time.ctime() 
            Time = "\"" + str(time_c) + "\""
            hectopascals = (random.random() * 15)
            humidity = (random.random() * 20)
            mositure = (random.random() * 30)
            light = (random.random() * 30)
            degrees = (random.random() * 30)
            # Build the message with simulated telemetry values.
            row_data = data.iloc[i]
            row_data = tuple(row_data)
            msg_txt_formatted = MSG_TXT % row_data
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if degrees > 30:
              prop_map.add("temperatureAlert", "true")
            else:
              prop_map.add("temperatureAlert", "false")

            # Send the message.
            # print( "Sending message: %s" % message.get_string() )
            # client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(10)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
