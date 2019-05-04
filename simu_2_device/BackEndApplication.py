import sys
import time

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_service_client
# pylint: disable=E0611
from iothub_service_client import IoTHubDeviceMethod, IoTHubError
from builtins import input

# The service connection string to authenticate with your IoT hub.
# Using the Azure CLI:
# az iot hub show-connection-string --hub-name {your iot hub name}
CONNECTION_STRING ="HostName=Trail427.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=u1Mw/re41ohOmfw7YHBCfLMpaWKjB/YQNlHbDdqXYbA="
DEVICE_ID = {}
DEVICE_ID[1] = "sim1"
DEVICE_ID[2] = "sim2"

# Details of the direct method to call.
#METHOD_NAME = "SetTelemetryInterval"
METHOD_NAME = "test latency"
METHOD_PAYLOAD = "5"
TIMEOUT = 5

def iothub_devicemethod_sample_run(myindex):
    try:
        # Connect to your hub.
        iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)

        # Call the direct method.
        response = iothub_device_method.invoke(DEVICE_ID[myindex], METHOD_NAME, METHOD_PAYLOAD, TIMEOUT)

        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(METHOD_NAME) )
        print ( "Device Method payload    : {0}".format(METHOD_PAYLOAD) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )
        print ( "Response payload         : {0}".format(response.payload) )
        return True

    #input("Press Enter to continue...\n")

    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return False
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )


def iothub_device_askdata(myindex):
    iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)
    response = iothub_device_method.invoke(DEVICE_ID[myindex], "send_file", str(myindex), TIMEOUT)
    try:
        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format("send_file") )
        print ( "Device Method payload    : {0}".format(str(myindex)) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )
        print ( "Response payload         : {0}".format(response.payload) )
        return True
    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return False
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )



if __name__ == '__main__':
    print ( "IoT Hub Python quickstart #2..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )
    
    print ("sending test to device 1")
    isconnect = iothub_devicemethod_sample_run(1)
    if isconnect == True:
        iothub_device_askdata(1)
    time.sleep(5)
    print ("sending test to device 2")
    isconnect = iothub_devicemethod_sample_run(2)
    if isconnect == True:
        iothub_device_askdata(2)
