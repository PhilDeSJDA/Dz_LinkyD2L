
# DzLinkyD2L


(English Later, Linky is so ... "*Frenchie*")  
Intégration dans **Domoticz** de l'interface temps réel avec Linky que propose le module D2L d'eeSmart (~50€) , voir ici  [http://eesmart.fr/modulesd2l/erl-wifi-compteur-linky/](http://eesmart.fr/modulesd2l/erl-wifi-compteur-linky/),  et propose un suivi temps réel en consultation sur son site web : *consospy*  
Ce module est d'ores et déjà intégré pour eeDomus.  
Il s'agit de créer un plugin qui permettra de disposer en temps réel dans *Domoticz* des principales données de Linky et de pouvoir ainsi bénéficier de ses services (Alertes/Notification/Historisations) et scripting (Lua/Blocky) 
J'ai débuté l'intégration mi Juillet Et ça a l'air de commencer à (bien) fonctionner (version Raspberry).  
On crée un répertoire dans domoticz/plugins ... LinkyD2L par exemple. Dans domoticz on ajoute le Hardware D2L et ca fait ... des choses
## Installation
Copier dans le répertoire des plugins que vous avez créé (*domoticz/plugins/LinkyD2L*), les fichiers suivants :
 - plugin.py : le code principal
 - D2L.py : le "poisson pilote" du précédent (le code de ce que je ne suis pas arrivé à intégrer facilement dans le plugin)  
Dans Domoticz Hardware (Matériel) Installer le plugin **D2L pour  Linky**, en renseignant vos codes **consospy** . 3 Devices (Dispositifs) seront alors créés dans l'onglet Utility (Mesures) :  
Il sont préfixés par "D2L - ", vous pourrez les renommer dans l'onglet Devices  (Dispositifs)
 - **LKY_Watts** : consommation instantanée 
 - **LKY_Amperes** : suivi de l'intensité consommée en temps réel
 - **LKY_IndexKWH** : valeur de l'index Enedis
 Les deux modules python communiquent via un fichier créé dans leur répertoire : *D2L.json* . sa forme lisible *D2L.txt* est également disponible dans le répertoire
## Aperçus

[Parametrage de l'installation](https://github.com/PhilDeSJDA/Dz_LinkyD2L/blob/master/LinkyD2L_Create.png)  
[Les 3 devices dans Utility](https://github.com/PhilDeSJDA/Dz_LinkyD2L/blob/master/LinkyD2L_Utility.png)  
[Suivi de la consommation](https://github.com/PhilDeSJDA/Dz_LinkyD2L/blob/master/LinkyD2L_Watts.png)  
[Suivi de l'Ampérage](https://github.com/PhilDeSJDA/Dz_LinkyD2L/blob/master/LinkyD2L_Amperes.png)



<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA2MzIxODQxNCwtODI3MjcyNTgzLDIxMj
MwNjY4NDAsLTIwMjY3MDE0MTYsMTEwMDQwMjAwMywxNzg1MzM3
MTEwLC0xMjQ1NzYzMzI4LDExNzY1NjI4MDUsMTg3NjM4ODMyMy
w0MTYwNzExODgsMTExNDM4OTAzMCw1ODE5NzQ5NzgsNjQ0ODQ4
MDQwLC04OTUxNTAxNTAsLTE2OTc3MTk1NDcsMTY5OTUxMzgyMy
wtNDk4MTcxNDg4XX0=
-->