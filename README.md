# Rattrapage SeR
## Installation
 ` pip install -r requirements.txt  `
 
 Nécessite :
 - tqdm : barre de progrès 
 - gym : Pour moi plus tard, donne une interface pour coder l'environnement pour tester d'autre méthodes
 - numpy : matrices
 - matplolib : visualisation de la séquence d'algorithme génétique
 - pandas : pour l'extraction d'excel
 
## Utilisation
Dans un invité de commande dans le dossier du projet:

  `python genetic.py `
  
  Il faudra ensuite choisir quelle instance de données utiliser : 
  Taper S pour la petite
  Taper G pour la grande
  
  La population est ensuite initialiser avec les paramètres rensignés dans le fichier config.py
  
  La taille de population par défaut est 100
  
  Puis, 3 choix s'offrent à vous :
  - faire 1 génération : taper 'G'
  - faire 100 générations : taper 'C'
  - arreter l'algorithme et sortir le fichier matlplotlib.
    Par défaut le fichier s'appelle genetic.png
    
    