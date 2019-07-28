
**

# DzLinkyD2L


(English Later, Linky is so Frenchie)
Intégration dans **Domoticz** de l'interface temps réel avec Linky que propose le module D2L d'eeSmart  ( [http://eesmart.fr/gammes/d2l/]) pour environ 50€ et propose un suivi temps réel sur un site web : consospy  

Ce module est d'ores et déjà intégré pour eeDomus.  
Il s'agit de créer un plugin qui permettra de disposer en temps réel dans Domoticz des principales données de Linky et d'ainsi de pouvoir bénéficier des services de Dz (Alertes/Notification/Historisations) et scripting (Lua/Blocky) 
J'ai débuté l'intégration mi Juillet Et ça a l'air de commencer à (bien) fonctionner (version raspberry).  On crée un répertoire dans domoticz/plugins ... LinkyD2L par exemple. Dans domoticz on ajoute le Hardware D2L et ca fait ... des choses
## Installation
Copier dans le répertoire des plugins de Domoticz (domoticz/plugins), les fichiers suivants
 - plugin.py : le code principal
 - D2L.py : le "poisson pilote" du précédent (le code de ce que je ne suis pas arrivé à intégrer facilement dans le plugin)
Dans Domoticz Installer le Hardware D2L, en renseignant vos codes **consospy** . 3 "devices" seront alors créés :
 - **LKY_Watts** : consommation instantanée 
 - **LKY_Amperes** : suivi de l'intensité consommée en temps réel
 - **LKY_IndexKWH** : valeur de l'index Enedis
 Les deux modules python communiquent via un fichier créé dans leur répertoire : *D2L.json* . sa forme lisible *D2L.txt* est également disponible dans le répertoire
## Aperçu

[Le suivi journalier de la consommation](https://github.com/PhilDeSJDA/Dz_LinkyD2L/blob/master/LKY_watts.png)


<!--stackedit_data:
eyJoaXN0b3J5IjpbMTYwMTMzMTUyMCw2MTk3NzIyNTQsLTQzNT
YyNTkzNiwtMTUxMDI1OTkyNCwtMTA4NjgzNTA2NCwxMjg3MTQz
NjYxLDEwNzcyOTU4NTYsMTcxODE4NjU0OSwtMjc0MTkxMzgxLC
01NjgwODQwMV19
-->