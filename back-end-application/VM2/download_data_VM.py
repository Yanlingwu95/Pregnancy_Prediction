# Download data file from blob

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
# import pandas as pd
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import pickle

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

CONNECTION_STRING ="HostName=Trail427.azure-devices.net;DeviceId=sim4;SharedAccessKey=k7xW31tFXnu9LflCN8iVk/zvjd2xGzTcdka7OGJdWsw="
# CONNECTION_STRING = "HostName=CC-project-hub.azure-devices.net;DeviceId=Raspberry-Pi;SharedAccessKey=L0roOnzlbkhvu3O6GSKWMMcwTTu06Rh2IKeQingYXzs="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# global file_output
global count
count = 0
def ML_prediction(filename, classifier):
    data = pd.read_csv(filename)
    trn = data.iloc[:,1:-1]
    pickle_file = open(classifier,'rb')
    clf = pickle.load(pickle_file)
    label = clf.predict(trn)
    with open("pre_result.txt","w") as f:
        f.write("pregnant_cow_ID \t Group_ID\n")
        f.close()
    with open("pre_result.txt","a") as f:
        for i in range(len(label)):
            if label[i] == 0:
                f.write(str(i)+"\t"+str(i+10)+"\n")
        f.close()


def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

# Handle direct method calls from IoT Hub
def device_method_callback(method_name, payload, user_context):
    global INTERVAL
    global count
    error = False
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s" % (method_name, payload) )
    # print ("Hello World\n")
    device_method_return_value = DeviceMethodReturnValue()
    
    ## Upload file to blob on Azure
    if method_name == "make_classify":
        filename = payload.split(" ")[-1][:-2]
        print("filename: {}".format(filename))
        count += 1
        block_blob_service = BlockBlobService(account_name='storageaccounttwo', account_key='ADlr/xU11oIjkx6QFL/ZCX+EJ/UZHUiV45gIDXAj124MyHHV/FgsSBQ3OEkpaEahwtrb0XWRUbgML3e1uO2fag==')
        block_blob_service.get_blob_to_path(
                                            'blob2', #blob name
                                            filename, #blob's file name   
                                            'real_time_data'+str(count)+'.csv' # local file name          
                                            )
        response = 'OK'
        print("Download Successfully!!")
        ML_prediction('real_time_data2.csv','ML_Model_DecisionTree.pickle')
        print("prediction Successfully!!!")
        sendemail_attachment.sendemail()
        print("Sent email Successfully!!")

    else:
        response = 'unknown command'
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
        while (True):
            time.sleep(10)
            print("waiting for command")

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )



if __name__ == '__main__':
    print ( "VM2--Running--Waiting for command to Download data" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()

