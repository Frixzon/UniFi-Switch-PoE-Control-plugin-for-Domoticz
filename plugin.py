#
#   Ubiquiti Plugin
#
#   Frix, 2020
#

"""
<plugin key="ubiquiti" name="UniFi Switch - POE Control" author="Frix" version="0.1">
    <description>
        <h2>Ubiquiti UniFi Switch - POE Control</h2><br/>
        Creates four switches to control each POE port on your UniFi Switch US-8. Possible commands are On / Off. Make sure to turn on SSH in your switch and enter the address, username and password in the fields below.
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="192.168.1.2"/>
        <param field="Username" label="User" width="200px" required="true" default=""/>
        <param field="Password" label="Password" width="200px" required="true" default=""/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
                <option label="Logging" value="File"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import urllib.request
from pexpect import pxssh
import sys,os
import threading
import queue

class UbntPlugin:
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Heartbeat(10)

        if (len(Devices) == 0):
            Domoticz.Device(Name="PoE 1", Unit=5, TypeName="Switch").Create()
            Domoticz.Device(Name="PoE 2", Unit=6, TypeName="Switch").Create()
            Domoticz.Device(Name="PoE 3", Unit=7, TypeName="Switch").Create()
            Domoticz.Device(Name="PoE 4", Unit=8, TypeName="Switch").Create()

        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)

    def onStop(self):
        Domoticz.Debug("onStop - Plugin is stopping.")

    def onCommand(self, Unit, Command, Level, Hue):
        con = pxssh.pxssh(encoding='utf-8')
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        #login to switch
        Domoticz.Debug("connecting to "+str(Parameters["Address"])+"...")
        con.login(Parameters["Address"], Parameters["Username"], Parameters["Password"], auto_prompt_reset=True)
        if "Switch8-Port60W" in con.before:
            Domoticz.Debug("logged in on")
            con.sendline('telnet localhost')
            con.sendline('enable')
            con.sendline('configure')
            con.sendline('interface 0/'+str(Unit))
            if str(Command).lower() == "off":
                con.sendline('poe opmode shutdown')
                Devices[Unit].Update(nValue=0, sValue="Off", TimedOut=0)
            else:
                con.sendline('poe opmode auto')
                Devices[Unit].Update(nValue=1, sValue="On", TimedOut=0)

global _plugin
_plugin = UbntPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return