# RaspberryPi controller of a LED using the MQTT protocol
A Swift app able to control a LED, connected to GPIO pins on a Raspberry Pi using a MQTT protocol

## About Swift
Swift is a fantastic way to write software, whether it’s for phones, desktops, servers, or anything else that runs code. It’s a safe, fast, and interactive programming language that combines the best in modern language thinking with wisdom from the wider Apple engineering culture and the diverse contributions from its open-source community. The compiler is optimized for performance and the language is optimized for development, without compromising on either.

## About this project
So the basic idea behind this project was to make use of the stuff most of tech geeks have lying around at home. In this case it was a Raspberry Pi 3, an SD card, a power brick, a breadboard, some wires and one or more LED diods. The concept is simple create an app which can comunicate with the Raspberry Pi and instruct it to trigger the GPIO pin to turn the LED on or off.

## Setting the environment
1. Firstly we need to setup the environment we will be working in. In this case it is Raspbian Bullseye. We flash it to the SD card and it is ready to boot. After we configured the OS we can install some packages needed to complete this project.

2. We install the Mosquitto MQTT server in the terminal from the repository `wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key`. After the installation is complete we can check the funcionality typing `mosquitto -v` into the terminal and we get:

![snipp](https://user-images.githubusercontent.com/54951169/150240486-bdf48621-ed3c-403d-8956-255df23b689e.png)

3. The next step is to create an app in Xcode. After we createt a new project we add a podfile to be able to open the `.xcworkspace` file.

```swift

import UIKit
import CocoaMQTT


class ViewController: UIViewController {
    
   //Istantiate CocoaMQTT as mqttClient
    let mqttClient = CocoaMQTT(clientID: "Device", host: "192.168.1.13", port: 1883)
    
  
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func ledToggle(_ sender: UISwitch) {
        
        if sender.isOn{
            mqttClient.publish("LED is:", withString: "On")
            print ("LED is on.")
        }
        else {
            mqttClient.publish("LED is:", withString: "Off")
            print ("LED is off.")
            }
        }
    
    @IBAction func connectButton(_ sender: UIButton) {
        if (mqttClient.connect()){
            print ("Connection succesful!")
        }
        else {
            print ("Connection failed!")
        }
        }
    @IBAction func disconnectButton(_ sender: UIButton) {
       if mqttClient.connect() == true{
           mqttClient.disconnect()
           print ("Disconnected!")
        }
        else {
           print ("Device was not connected!")
        }
     
    }
}

```

PYTHON

```python
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
clientName = "Device"

#set MQTT server adress
serverAddress = "192.168.0.12"

#instantiate Eclipse Paho as mqttClient
mqttClient = mqtt.Client(clientName)

#set calling functions  to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

#connect client to server
mqttClient.connect(serverAddress)

#monitor client activity forever
mqttClient.loop_forever()

```

![ezgif-7-38a182911e](https://user-images.githubusercontent.com/54951169/150238291-1e1f3738-4700-4f3e-bd4d-aca86de60332.gif)

![ezgif-7-2786a1e56b](https://user-images.githubusercontent.com/54951169/150238720-570f035e-a092-4c31-bda1-41013e5b27db.gif)

![ezgif-7-f8e0e5440a](https://user-images.githubusercontent.com/54951169/150238276-149dca96-dabb-4322-b872-28a167b55068.gif)


![ezgif-7-7effcdcfd6](https://user-images.githubusercontent.com/54951169/150238733-f3690130-a817-4fbb-911d-86228c23012c.gif)
