import time
import sys
import iothub_client
import os
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult, IoTHubError

# CONNECTION_STRING = "HostName=Trail413.azure-devices.net;DeviceId=mynewdevice;SharedAccessKey=NYoyx/ib9kq1og6eDwIRXgwd4zCQmEnINLGtrSoUAdk="
CONNECTION_STRING = "HostName=Trail413.azure-devices.net;DeviceId=mynewdevice;SharedAccessKey=NYoyx/ib9kq1og6eDwIRXgwd4zCQmEnINLGtrSoUAdk="
# CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=cs2743a315b9ea3x49fdxb30;AccountKey=fiGff9v/aulWyb6T3eUupbS4hS2ygfwmTmAQ55+xA+q+enpqIJfaPRfqSQ9paP2idEoj+FYaU7wX+FWWHfSkPQ==;EndpointSuffix=core.windows.net"

PROTOCOL = IoTHubTransportProvider.MQTT

PATHTOFILE = "./row_data.json"

FILENAME = "row_data.json"


def blob_upload_conf_callback(result, user_context):
    if str(result) == 'OK':
        print ( "...file uploaded successfully." )
    else:
        print ( "...file upload callback returned: " + str(result) )

def iothub_file_upload_sample_run():
    try:
        print ( "IoT Hub file upload sample, press Ctrl-C to exit" )

        client = IoTHubClient(CONNECTION_STRING, PROTOCOL)

        f = open(PATHTOFILE, "r")
        print("Open file successfully!!!!!!!!!!!!!!!!!")
        content = f.read()

        client.upload_blob_async(FILENAME, content, len(content), blob_upload_conf_callback, 0)

        print ( "" )
        print ( "File upload initiated..." )

        while True:
            time.sleep(30)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
    except:
        print ( "generic error" )

if __name__ == '__main__':
    print ( "Simulating a file upload using the Azure IoT Hub Device SDK for Python" )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_file_upload_sample_run()