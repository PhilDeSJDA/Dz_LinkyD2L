# Basic Python Plugin Example
#
# Author: Philou55 sur base GizMoCuz
#
# Le 
#
"""
<plugin key="LinkyD2L" name="D2L pour Linky" author="Philou55" version="1.0.0">
    <description>
        Declarez le D2L avec vos identifiants ConsoSpy et vous obtiendrez
        <ul style="list-style-type:square">
                <li>votre index de relève en temps réel</li>
        </ul>
    </description>
    <params>
         <param field="Username" label="Identifiant" width="100px" required="true" default=""/>
         <param field="Password" label="mot de passe" width="100px" required="true" default=""/>
         <param field="Mode1" label="Scan Delay (mn)" width="20px" required="true" default="1"/>
         <param field="Mode2" label="Debug  Y/N"  width="20px" required="true" default="N"/>
    </params>
</plugin>
"""

import Domoticz
import json
import os
import datetime

#import requests

class BasePlugin:

    # controle du heartbeat
    flag01 = 0
    nflag01 = 6
    sMins = None 
    path = None
    sUser = None
    sPassword = None
    sDebug = None
    debug = False
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        self.flag01=0
        # self.nflag01 = int(Parameters["Frequence"])
        Domoticz.Heartbeat(20)
        self.path=os.getcwd() + "/plugins/LinkyD2L"
        self.sUser=Parameters["Username"]
        self.sPassword=Parameters["Password"]
        self.sMins=Parameters["Mode1"]
        self.nflag01 = int(self.sMins) * 3
        self.sDebug=Parameters["Mode2"].upper()
        if self.sDebug == "Y" : self.debug=True
        Domoticz.Log("START with (" + self.sUser+","+self.sPassword+") scan every "+self.sMins+" mn ("+str(self.nflag01)+ "HB) , Debug="+self.sDebug)

        if(len(Devices)==0): 
           Domoticz.Device(Name="D2L_Index",  Unit=1, TypeName="Custom").Create()
           Domoticz.Device(Name="D2L_Intens",  Unit=2, TypeName="Current/Ampere").Create()
           Domoticz.Device(Name="D2L_Watt",  Unit=3, TypeName="kWh").Create()
  
        if self.debug: DumpConfigToLog()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        if self.flag01 == 0:
          script=self.path + "/D2L.py"
          res=os.system("python " + script + " " + self.sUser + " "+ self.sPassword)
          if self.debug: Domoticz.Log(script+"Result is "+str(res))

          fichier=(self.path + "/" + "D2L.txt")
          if os.path.isfile(fichier):
            with open(fichier) as json_file:
              data = json.load(json_file) 
            # Domoticz.Log(data['Heure']+"="+data['Index'])
            # index recupere par GetIndexBetween
            ix0=data['Index0'].split("=")
            nValue=float(ix0[1])/1000.
            #Domoticz.Log(str(nValue)+ " Kwh")
            Devices[1].Update(nValue=int(data['Index']),sValue=str(nValue))
            # intensite du courant
            sValue2=data['Courant']+";0;0"
            Devices[2].Update(nValue=int(data['Courant']),sValue=sValue2)
            #Domoticz.Log(Devices[2].Name+" : "+sValue2)
            # calcul de la puissance en WH
            ix1=data['Index1'].split("=")
            conso=int(ix0[1]) - int(ix1[1])
            #Domoticz.Log(str(ix0[0]) + " , " + str(ix1[0]))
            dat0 = datetime.datetime.strptime(ix0[0],'%Y-%m-%dT%H:%M:%S')
            dat1 = datetime.datetime.strptime(ix1[0],'%Y-%m-%dT%H:%M:%S')
            duree=(dat0-dat1).seconds
            if int(duree) != 0 :
              instantwatt=float(conso)*3600/float(duree)
              #Domoticz.Log("Conso:"+str(conso)+" de "+ix1[0]+" a "+ix0[0]+" soit "+ str(duree)+ "==> " +str(instantwatt))
              sValue3=str(instantwatt)+";"+str(nValue*1000)
              Devices[3].Update(nValue=0,sValue=sValue3)
              #Domoticz.Log(Devices[3].Name+" ==> "+sValue3)
            # trace pour florent
            # Domoticz.Log("Florent -->  Lastindex : " + data['Heure'] + ":" + data['Index'] + ", IndexsBetween(0) : " + data['Index0'])
          else:
            Domoticz.Log("fichier D2L.txt inexistant")
        
        self.flag01 = self.flag01 + 1
        if self.flag01 >= self.nflag01: self.flag01=0


global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Log( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Log("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Log("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Log("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Log("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Log("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Log("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Log("Device LastLevel: " + str(Devices[x].LastLevel))
    return
