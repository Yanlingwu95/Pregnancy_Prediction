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

CONNECTION_STRING ="HostName=myhob.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=Ymm95CVG0UuLd2pZNpg5OYQ+7JHqdgpaHJwBf5bcsBI="
DEVICE_ID = "ippot"
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
    block_blob_service = BlockBlobService(account_name='cs2001bdb3eb2d4x451dxa02', account_key='3c5UthTVHRPvjI65OWRxIxiJSDASv/G8byG1uGjn0AYxR2KgRCo1EKh4AdWQT4xwV7Z4i7bxO7SAFDTF+VANgQ==')

    block_blob_service.get_blob_to_path('data', '0_99060ec4216d4ee5a9515e5495a93dd9_1.json', 'down_data')

    f=open("down_data")
    temp=[]
    hum=[]
    time=[]
    pressure=[]
    light=[]
    moisture=[]
    import json
    for line in f:
        d = json.loads(line)
        temp.append(d['Temp'])
        time.append(d['Time'])
        hum.append(d['Humidity'])
        pressure.append(d['Pressure'])
        moisture.append(d['Moisture'])
        light.append(d['Light'])

##print (temp,time,hum,pressure,moisture,light)

    cur_temp = sum(temp[-2:])/2.
    cur_hum = sum(hum[-2:])/2.
    cur_pressure = sum(pressure[-2:])/2.
    cur_moisture = sum(moisture[-2:])/2.
    cur_light = sum(light[-2:])/2.

    Myfunc=""
    Myload="10"
    print (cur_temp)
    if cur_temp<21: Myfunc=Myfunc+"Tup "
    elif cur_temp>24: Myfunc=Myfunc+"Tdown "
    else: Myfunc=Myfunc+"Tst "
    if cur_hum<24: Myfunc=Myfunc+"Hup "
    elif cur_hum>22: Myfunc=Myfunc+"Hdown "
    else : Myfunc=Myfunc+"Hst "
    if cur_moisture>600: Myfunc=Myfunc+"Mdown "
    elif cur_moisture<300: Myfunc=Myfunc+"Mup "
    else: Myfunc=Myfunc+"Mst "
    if cur_light<450: Myfunc=Myfunc+"Lup "
    elif cur_light>550: Myfunc=Myfunc+"Ldown "
    else: Myfunc=Myfunc+"Lst "

    print (time[-1])
    print ( "IoT Hub Python quickstart #2..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )
    print (Myfunc)
    iothub_devicemethod_sample_run(Myfunc,Myload)
