import sys
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_service_client
# pylint: disable=E0611
from iothub_service_client import IoTHubDeviceMethod, IoTHubError
from builtins import input
from azure.storage.blob import BlockBlobService

CONNECTION_STRING ="HostName=Trail413.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=C0x4dayT2cVHYkckVoSLDNo35p9yP/Jc7x8Dhq89kgU="
DEVICE_ID = "mynewdevice"
TIMEOUT=60




def iothub_devicemethod_sample_run(Myfunc,Myload):
    try:
        # Connect to your hub.
        iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)

        # Call the direct method.
        response = iothub_device_method.invoke(DEVICE_ID,Myfunc, Myload, TIMEOUT)

        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(Myfunc ))
        print ( "Device Method payload    : {0}".format(Myload) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )
        print ( "Response payload         : {0}".format(response.payload) )

        input("Press Enter to continue...\n")

    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )


if __name__ == '__main__':
    block_blob_service = BlockBlobService(account_name='cs2743a315b9ea3x49fdxb30', account_key='fiGff9v/aulWyb6T3eUupbS4hS2ygfwmTmAQ55+xA+q+enpqIJfaPRfqSQ9paP2idEoj+FYaU7wX+FWWHfSkPQ==')
    block_blob_service.get_blob_to_path('mydata', 'firstdata.json', 'first_down_data')

    f=open("first_down_data")
    

    print (time[-1])
    print ( "IoT Hub Python quickstart #2..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )
    print (Myfunc)
    iothub_devicemethod_sample_run(Myfunc,Myload)
