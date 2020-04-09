# UniFi-Switch-PoE-Control-plugin-for-Domoticz
A Domoticz plugin that creates four switches to control each POE port on your UniFi Switch US-8. Possible commands are On / Off.

## Prerequisites
1. Make sure to turn on SSH in your switch: https://community.ui.com/questions/SSH-to-unifi-switches/2d179c83-fe11-4770-8c53-2f59bc4f5a5e
1. Rrequests libary for Python 3: https://pypi.org/project/requests/
1. pxssh libary for Python 3: https://pypi.org/project/pexpect/

## Installation
1. Clone repository into your Domoticz plugins folder
    ```
    cd domoticz/plugins
    git clone https://github.com/Frixzon/UniFi-Switch-PoE-Control-plugin-for-Domoticz.git
    ```
1. Restart domoticz
    ```
    sudo service domoticz.sh restart
    ```
1. Make sure that "Accept new Hardware Devices" is enabled in Domoticz settings
1. Go to "Hardware" page
1. Enter the Name
1. Select Type: `UniFi Switch - POE Control`
1. Click `Add`

## Update
1. Go to plugin folder and pull new version
    ```
    cd domoticz/plugins/UniFi-Switch-PoE-Control-plugin-for-Domoticz
    git pull
    ```
1. Restart domoticz
    ```
    sudo service domoticz.sh restart
    ```

## Devices
The following devices are created:

| Type                | Name                      | Description
| :---                | :---                      | :---
| Switch | Ubnt Switch - PoE #                     | Can turn On or Off the POE on the specific port number
