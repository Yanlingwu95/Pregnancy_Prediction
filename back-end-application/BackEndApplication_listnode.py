# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import sys
import time
import iothub_service_client
from iothub_service_client import IoTHubDeviceMethod, IoTHubError
from builtins import input
import sendmail

# The service connection string to authenticate with your IoT hub.
# Using the Azure CLI:
# az iot hub show-connection-string --hub-name {your iot hub name}
CONNECTION_STRING ="HostName=Trail427.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=u1Mw/re41ohOmfw7YHBCfLMpaWKjB/YQNlHbDdqXYbA="
DEVICE_ID = {}
DEVICE_ID[1] = "sim1"
DEVICE_ID[2] = "sim2"
DEVICE_ID[3] = "sim3"

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

        # print ( "" )
        # print ( "Device Method called" )
        # print ( "Device Method name       : {0}".format(METHOD_NAME) )
        # print ( "Device Method payload    : {0}".format(METHOD_PAYLOAD) )
        # print ( "" )
        # print ( "Response status          : {0}".format(response.status) )
        # print ( "Response payload         : {0}".format(response.payload) )
        return True
    #input("Press Enter to continue...\n")
    except IoTHubError as iothub_error:
        # print ( "" )
        # print ( "Unexpected error {0}".format(iothub_error) )
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
        #print ( "Unexpected error {0}".format(iothub_error) )
        print ("no connection")
        return False
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )


class ListNode(object):
    def __init__(self,data):
        self.val = data
        self.left = None
        self.right = None

class Queue(object):
    def __init__(self):
        self.head = None
        self.tail = None
    def push(self,node):
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.right = node
            node.left = self.tail
            self.tail = node
            node.right = None
    def pop(self):
        ret = self.head
        self.head = ret.right
        ret.left = None
        ret.right = None
        if self.head!=None:
            self.head.left = None
        return ret

def swap(queue):
    tem = queue.pop()
    queue.push(tem)


def testlatency(myindex):
    isconnect = iothub_devicemethod_sample_run(myindex)
    return isconnect

def askfordata(myindex):
    iothub_device_askdata(myindex)
    print ("finish sending data")



if __name__ == '__main__':
    print ( "IoT Hub Python quickstart #2..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )
    
    latencyref = {}
    myqueqq = Queue()
    for i in range(3):
        latencyref[i+1] = 0
        node = ListNode(i+1)
        myqueqq.push(node)
    sendpointer = myqueqq.head
    for i in range (50): #while true
        for j in range(6):  #
            print ("ping Pi ",sendpointer.val)
            isconnect = testlatency(sendpointer.val)
            if isconnect:
                print ("success")
                askfordata(sendpointer.val)
                swap(myqueqq)
                sendpointer = myqueqq.head
                break
            else:
                latencyref[sendpointer.val]+=1
                ti = latencyref[sendpointer.val]
                print ('pi ',sendpointer.val,'failed, it is the ',ti,' times it failed\n')
                if ti == 3:
                    print ("pi ",sendpointer.val,"is extremely destoryed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
                    message = "pi " + sendpointer.val + "is extremely destoryed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    sendmail.sendemail(message)
                    print("send successfully!!!")
                swap(myqueqq)
                sendpointer = myqueqq.head
            time.sleep(2)
        time.sleep(15)
