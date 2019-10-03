#
#	D2L.py : le poisson pilote de l integration du D2L de "eesmart" dans Domoticz
#	Ce module independant sera appeler par le plugin Domoticz
#	Il consomme les API du site consospy et transmet a Domoticz
#
#	1 arg1  Identifiant Consospy
#       2 arg2  Mot de passe Consospy
#       3 arg3  Nombre de minutes a extraire (facultatif)
#
#       1.0.2   protection contre un date non initialisee, a voir avec le support
#       1.0.3   protection contre une intensite a 'None'
#


import requests
import json
import datetime
import sys
import os

def error_exit(status,message):
  res_dict = { "status" : status , "erreur" : message , "version" : version }
  f=open(outFile,"w")
  f.write(json.dumps(res_dict))
  f.close()
  f=open(txtFile,"w")
  f.write(str(res_dict).replace(",","\n"))
  f.close()
  exit(status)

#
#   Constantes et autres
#

#path="/home/pi/domoticz/plugins/LinkyD2L"
version = "1.0.3"
script  = os.path.realpath(__file__)
path=os.path.dirname(script)
txtFile = path + "/D2L.txt"
outFile = path + "/D2L.json"
apiBase='https://consospyapi.sicame.io/api/D2L'
apiB=apiBase + '/D2LS'
# Recuperation des identifiants consospy
if len(sys.argv) < 3 :  error_exit(1,"Pas assez de parametres")

sLogin=sys.argv[1]
sPassword=sys.argv[2]
nIX = 1

if len(sys.argv) >= 4 :
  nIX=int(sys.argv[3])
  if nIX < 6:
    nIX = 6
  if nIX > 99:
    nIX = 99

# Recuperation de l'ApiKey de consospy

headers = {
        'accept': 'text/plain',
        'Content-Type': 'application/json-patch+json',
          }
data = '{ "login":"' + sLogin + '" , "password":"' + sPassword + '" }'
response = requests.post(apiBase + '/Security/GetAPIKey', headers=headers, data=data)

if response.status_code != 200 : error_exit(2,"Identifiants incorrects")
j=json.loads(response.text)
apiKey=j['apiKey']

headers = {
        'accept' : 'text/plain',
        'Content-Type': 'application/json-patch+json',
        'APIKey' : apiKey,
         }
    
data = '{}'

response = requests.get(apiB, headers=headers, data=data)
if response.status_code != 200 : error_exit(3,str(reponse.status_code)+" Lecture caracteristiques D2L")


j=json.loads(response.text)
u=j[0]
idModule=str(u['idModule'])
Label=u['labelModule']
Compteur=str(u['counter'])

response = requests.get(apiB +'/'+ str(idModule) + '/TypeContrat', headers=headers, data=data)
if response.status_code != 200 : error_exit(4,str(reponse.status_code)+" Lecture type contrat")
Contrat=response.text

response = requests.get(apiB+'/' + str(idModule) + '/LastIndexes', headers=headers, data=data)
if response.status_code != 200 : error_exit(5,str(reponse.status_code)+" Lecture dernier index")
j=json.loads(response.text)
jsave=j
Index=str(j['baseHchcEjphnBbrhcjb'])

response = requests.get(apiB+'/' + str(idModule) + '/LastCurrents', headers=headers, data=data)
if response.status_code != 200 : error_exit(6,str(reponse.status_code)+" Lecture dernieres intensites")
j=json.loads(response.text)
Intensite=str(j['iinst1'])
if Intensite == 'None' : Intensite='0'

hr=str(j["horloge"])
# suite probleme de epierre 09/2019
if hr == '0001-01-01T00:00:00' : hr=str(jsave["horloge"])

sDate=hr[0:10]
sHour=hr[11:19]

# recuperation d'indexs
dob = datetime.datetime.strptime(hr, '%Y-%m-%dT%H:%M:%S')
sDob=str(dob.date()) + "T" + str(dob.time())
dob2 = dob - datetime.timedelta(minutes=nIX)
#print( datetime.timedelta(minutes=nIX))
sDob2=str(dob2.date()) + "T" + str(dob2.time())
adurl = "?from=" + sDob2 + "&to=" + sDob 
#print(adurl)
response = requests.get(apiB+'/' + str(idModule) + '/IndexesBetween' + adurl , headers=headers, data=data)
if response.status_code != 200 : error_exit(7,str(reponse.status_code)+" Lecture "+str(nIX)+" derniers indexs")
j=json.loads(response.text)

# production resultat
f=open(outFile,"w")
res_dict = {
    'status' : 0,
    'error' : 'no error', 
    'Version' : version ,
    'Date' :  sDate ,
    'Heure' : sHour ,
    'Name' :  Label ,    
    'D2L' :  idModule ,
    'Compteur' : Compteur ,
    'Contrat' :  Contrat ,
    'Index' :  Index ,
    'Courant' :  Intensite ,
    } 


i=0
res_dict.update( { "nIndex" : len(j) } )
while(i<len(j)):
  jkey="Index" + str(i)
  jdat=j[i]['horloge'] + "=" +str(j[i]['baseHchcEjphnBbrhcjb'])
  res_dict.update( { jkey : jdat } )
  i += 1

f.write(json.dumps(res_dict))
f.close()

f=open(txtFile,"w")
f.write(str(res_dict).replace(",","\n"))
f.close()


exit(0)


