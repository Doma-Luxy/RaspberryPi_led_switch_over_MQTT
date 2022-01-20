# RaspberryPi controller of a LED using the MQTT protocol
A Swift app able to control a LED, connected to GPIO pins on a Raspberry Pi using a MQTT protocol

## About Swift & MQTT
*Swift* is a fantastic way to write software, whether it’s for phones, desktops, servers, or anything else that runs code. It’s a safe, fast, and interactive programming language that combines the best in modern language thinking with wisdom from the wider Apple engineering culture and the diverse contributions from its open-source community. The compiler is optimized for performance and the language is optimized for development, without compromising on either.

*MQTT* is an OASIS standard messaging protocol for the Internet of Things (IoT). It is designed as an extremely lightweight publish/subscribe messaging transport that is ideal for connecting remote devices with a small code footprint and minimal network bandwidth. MQTT today is used in a wide variety of industries, such as automotive, manufacturing, telecommunications, oil and gas, etc.

To better understand the implementation on the MQTT protocol I used this book: [MQTT Essentials - A Lightweight IoT Protocol](https://books.apple.com/us/book/mqtt-essentials-a-lightweight-iot-protocol/id1198410878)

## About this project
So the basic idea behind this project was to make use of the stuff most of tech geeks have lying around at home. In this case it was a Raspberry Pi 3, an SD card, a power brick, a breadboard, some wires and one or more LED diods. The concept is simple create an app which can communicate with the Raspberry Pi and instruct it to trigger the GPIO pin to turn the LED on or off.

## Walkthrough from setting the environment on the Raspberry Pi to writing the app in Swift
1. Firstly we need to setup the environment we will be working in. In this case it is Raspbian Bullseye. We flash it to the SD card and it is ready to boot. After we configured the OS we can install some packages needed to complete this project.

2. We install the Mosquitto MQTT server in the terminal from the repository `wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key`. After the installation is complete we can check the funcionality typing `mosquitto -v` into the terminal and we get:

![snipp](https://user-images.githubusercontent.com/54951169/150240486-bdf48621-ed3c-403d-8956-255df23b689e.png)

3. The next step is to create an app in Xcode. After we created a new project we add a podfile to the folder through the terminal, to be able to open the `.xcworkspace` file. In the "Storyboard" we created the frontend layout of the app and assigned what the actions schould do. In this case the "ledToggle" is turning the LED on and of and the "Connect" and "Disconnect" buttons are initating and terminating the connection to the MQTT server.

```swift
import UIKit
import CocoaMQTT


class ViewController: UIViewController {
    
   //Istantiate CocoaMQTT as mqttClient
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host: "192.168.1.12", port: 1883)
    
  
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func ledToggle(_ sender: UISwitch) {
        
        if sender.isOn{
            mqttClient.publish("rpi/gpio:", withString: "On")
            print ("LED is on.")
        }
        else {
            mqttClient.publish("rpi/gpio:", withString: "Off")
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
We get this as a result of the comunication of the iOS device and the MQTT server:
![YmQyjOw](https://user-images.githubusercontent.com/54951169/150242093-ab6900e5-a5c5-4370-a03d-cd60346582c2.png)

4. To install the Python development tools we use the following command in the terminal: `sudo apt-get install python-dev`. After that we install the *Eclipse Paho* library using the command `pip install paho-mqtt`.

5. Then in the desired working folder we create a file gpioLED.py with the following code which will be in charge of comunicating with the app through the MQTT server.

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

```
6. Finally we can run the gpioLED.py from the terminal using the command: `sudo python3 gpioLED.py` and run the file. Then when the app is launched we can connect to the server using the "Connect" button of the app, when the app is connected we can toggle the switch on to turn on the LED, as shown below.

![ezgif-7-38a182911e](https://user-images.githubusercontent.com/54951169/150238291-1e1f3738-4700-4f3e-bd4d-aca86de60332.gif)

![ezgif-7-2786a1e56b](https://user-images.githubusercontent.com/54951169/150238720-570f035e-a092-4c31-bda1-41013e5b27db.gif)

![ezgif-7-f8e0e5440a](https://user-images.githubusercontent.com/54951169/150238276-149dca96-dabb-4322-b872-28a167b55068.gif)

![ezgif-7-7effcdcfd6](https://user-images.githubusercontent.com/54951169/150238733-f3690130-a817-4fbb-911d-86228c23012c.gif)
