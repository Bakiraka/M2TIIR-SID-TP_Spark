# M2 TIIR – SID 2015-2016 – TP Spark
**Auteurs** : Rokni Samansa, Djenane Anthony

> Le but de ce TP est d’expérimenter avec Spark pour nous familiariser avec la programmation répartie selon le modèle « Map Reduce ». Nous allons utiliser un jeu de données et créer un algorithme résolvant un problème défini pour ce jeu de données.


### Étape 1 : Téléchargement et installation de Spark sur une machine

La première étape pour l'utilisation de Spark va consister en son installation. Pour cela, il va falloir se rendre sur [la page de téléchargement](http://spark.apache.org/downloads.html) de Spark, sélectionner la version de Spark, son package type (ici, nous choisirons _Pre-build for  Hadoop 2.6 and later_) et enfin télécharger et extraire le fichier compressé contenant Spark :

Commandes réalisées pour le téléchargement :
* `wget http://mirrors.ircam.fr/pub/apache/spark/spark-1.6.0/spark-1.6.0-bin-hadoop2.6.tgz `
* `tar xvf spark-1.6.0-bin-hadoop2.6.tgz`

Il est préférable d'avoir openjdk d'installé pour le bon fonctionnement de Spark, cela se fait sur Debian avec la commande :
* `apt-get install openjdk-7-jre`


Démarrage d'un master : `./bin/start-master.sh`

Une fois le master démarré, il est possible d'accéder à son interface web ( http://localhost:8080 par défaut). Cette interface web va indiquer les informations sur le maître (**master**), ses esclaves (**slaves** ou **workers**) ainsi que sur les travaux réalisés.
Nous devons désormais ajouter un ou plusieurs slaves au master. Nous allons récupérer le fichier de configuration template (`cp ./conf/spark-env.sh.template ./conf/spark-env.sh`) et y ajouter (ou décommenter) une ligne avec `SPARK_WORKER_INSTANCES=2`, pour par exemple 2 slaves.

Démarrage des slaves : `./sbin/start-slaves.sh`

Une fois l'installation de Spark réalisée, il est désormais possible de soumettre des travaux au master de la façon suivante :

`MASTER=spark://sparkmachine:7077 ./bin/spark-submit examples/src/main/python/wordcount.py README.md`

ou bien

`./bin/spark-submit --master spark://sparkmachine:7077 examples/src/main/python/wordcount.py README.md`
> Ici, "sparkmachine" fait référence au nom de la machine sur laquelle tourne Spark

Il est également possible d'utiliser Spark en mode interactif avec les binaires **_spark-shell_** (en scala) ou **_pyspark_** (en python). Pour lancer le mode interactif en connexion avec le cluster (master/slaves), cette commande est utile : `./bin/spark-shell --master spark://IP:PORT`.

### Étape 2 : Présentation du jeu de données utilisé

Pour ce TP, nous avons décidé d'utiliser des données récupérées sur [le site du gouvernement américain](http://www.data.gov/), et non sur le site du gouvernement Français. Les données choisies sont celle d'une étude (LTCCS : _Large Truck Crash Causation Study_) basées sur trois ans de collection de données par le Ministère des Transports des États-Unis. Ces données sont la première étude nationale aux États-Unis ayant pour but de tenter de déterminer les évènement et facteurs contribuants à des accidents de la route importante impliquant des camions.

Le choix de ces données fut fait de par la documentation sur le jeu de données assez important ainsi que sur la quantité de données relativement correcte.

### Étape 3 : Problème définit

À partir des données choisies, nous avons définit comme problème de calculer le nombre total de gros camions impliqués dans les accidents recensés lors de l'étude. Ceux-ci sont référencés dans le fichier generalvehicle.txt, nous les identifiront grace aux colonnes GVEBodyType et RATWeight.

* La table _generalvehicle_ étant celle qui nous intéresse, elle contient les véhicules recencés dans les accidents (p205 du manuel des données)
* La colonne _GVEBodyType_ étant le type de véhicule (différents code par type de véhicules, cf p.232 du manuel des données)
* La colonne _RATWeight_ est un ratio utilisé dans le but de l'étude, seul	les valeurs suppérieurs à 0 sont à considérer comme valides

### Étape 4 & 5 : Algorithme de résolution utilisant Map Reduce

Voici l'algorithme utilisé pour résoudre le problème défini ci-dessus :

``` python
from pyspark import SparkContext
#Module for reducebykey function
from operator import add

#Context definition
sc = SparkContext(appName="truckcount")

# File reading
text_file = sc.textFile("/home/debian/data/data/generalvehicle.txt")

#filter out header
file_header = text_file.first()
data = text_file.filter(lambda x: x != file_header)

counted_tuples = data.map(lambda line: line.split("\t")) \
                     .filter(lambda x: x[5] >= '60' and x[5] <= '70' or x[5]==70 or x[5]==74 or x[5]==78 ) \
                     .filter(lambda x: x[60] > 0) \
                     .map(lambda x: x[5]) \
                     .map(lambda x: (x,1)) \
                     .reduceByKey(add) \
                     .collect()

print sum(pair[1] for pair in counted_tuples)
```

### Informations utilisées

* [Documentation de Spark](http://spark.apache.org/docs/latest/)
* [Spark Standalone](http://spark.apache.org/docs/latest/spark-standalone.html)
* [Données choisies ](http://catalog.data.gov/dataset?q=LTCCS&sort=score+desc%2C+name+asc) (Large Truck Crash Causation Study)
* [Manuel des données](http://ai.fmcsa.dot.gov/ltccs/data/documents/LTCCS_Manual_Public.pdf)
