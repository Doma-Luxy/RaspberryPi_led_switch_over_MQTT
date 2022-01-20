#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

def gpioSetup():
#set pin numbering ti Broadcom scheme
    gpio.setmode(gpio.BCM)

#set GPIO21 (pin 40) as an output pin
    gpio.setup(21, gpio.OUT)
 
#execute when a connection has been established to the MQTT server
def connectionStatus (client, userdata, flags, rc):
#subscribe client to a topic
    mqttClient.subscribe("rpi/gpio")

#execute when a message has been received from the MQTT server
def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    if message == "on":
      gpio.output(21, gpio.HIGH)
      print("LED is ON!")
    elif message == "off":
      gpio.output(21, gpio.LOW)
      print("LED is OFF!")
    else:
      print("Unknown message!")

#set up RPI GPIO pins
gpioSetup()

#set client name
clientName = "iOS Device"

#set MQTT server adress
serverAddress = "192.168.1.12"

#instantiate Eclipse Paho as mqttClient
mqttClient = mqtt.Client(clientName)

#set calling functions  to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

#connect client to server
mqttClient.connect(serverAddress)

#monitor client activity forever
mqttClient.loop_forever()
