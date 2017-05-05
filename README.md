# NAO-Foot-Equipe-X
Equipe X : ENSTA Bretagne UV 2.7 



Base de départ pour la compétition NAO Foot UV 2.7 2017

Trois nouveaux scénarios (dans le dossier scenes) vont vous aider à réaliser votre application 
- nao-UV27-2017-foot-1-robot.ttt  : Terrain, balle et un robot (port 11212)
- nao-UV27-2017-foot-2-robots.ttt : Terrain, balle et 2 robots (ports 11212 et 11216)
- nao-UV27-2017-foot-4-robots.ttt : Terrain, balle et 4 robots (ports 11212, 11214,11216 et 11218)

(Note la version 4 robots fonctionne quasiment car on atteint les limites du PC de salle info ... sur un PC de gamer ça fonctionne bien)

Synchronisation des projets 

Pour les responsables d'équipes:

git remote add upstream https://github.com/bnaozr/NAO-Foot-Equipe-X

git fetch upstream

git pull upstream master

git push

Les fichiers binaires (v-rep, naoqi et python naoqi ne sont plus dans le projet public), les archives (naoqi-20170505.tgz,  pynaoqi-20170505.tgz et  v-rep-20170505.tgz) peuvent être récupérées sur public/share au lien suivant :

/public/share/uv27rob/

ensuite se placer dans le répertoire NAO-Foot-Equipe-X
et faire les commandes

tar xfz pynaoqi-20170505.tgz

tar xfz naoqi-20170505.tgz

tar xfz v-rep-20170505.tgz

il est ensuite recommandé d'effacer les fichiers tgz

-----------------------------------------------

Les membres d'une équipe peuvent se synchroniser au projet global (commandes ci dessus) mais ils peuvent aussi se synchroniser sur le projet de leur responsable (remplacer bill par le responsable d'équipe) :

git remote add upstream https://github.com/bill/NAO-Foot-Equipe-X

git fetch upstream

git pull upstream master

git push



----
Quelques commentaires libres ...

ensta bretagne
coucou les loulous ! 
stratégie de la team : cuillères, tatane et fourchette pas de pitié !!!!!!
