//
//  ViewController.swift
//  LED
//
//  Created by Domagoj Veštić on 15.12.2021.
//

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
