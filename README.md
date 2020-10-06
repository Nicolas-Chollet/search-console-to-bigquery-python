# Google Search Console to BigQuery avec Python

Cet article est inspiré de celui-ci, que je vous invite à consulter : [https://medium.com/@singularbean/revisiting-google-search-console-data-into-google-bigquery-708a19e2f746](https://medium.com/@singularbean/revisiting-google-search-console-data-into-google-bigquery-708a19e2f746)

Ainsi que le Github associé : [https://github.com/benpowis/search-console-bq](https://github.com/benpowis/search-console-bq)

- L'original de cette page, en Français, se trouve à l'adresse : [https://www.unnest.co/dossiers/google-search-console-to-bigquery-avec-python/](https://www.unnest.co/dossiers/google-search-console-to-bigquery-avec-python/)
- La suite (déploiement dans Google App Engine) se trouve ici : [https://www.unnest.co/dossiers/tutoriel-deployer-une-application-python-avec-google-app-engine/](https://www.unnest.co/dossiers/tutoriel-deployer-une-application-python-avec-google-app-engine/)

## Pourquoi vouloir charger la donnée Google Search Console dans BigQuery ?

La donnée issue de Google Search console est précieuse. Il s'agit d'une des rares sources permettant de connaître les mots clé ayant généré des impressions et des clics dans Google vers votre site. Il est donc intéressant, dans le cadre d'un "Marketing Data warehouse", d'y déverser cette donnée.

Cela permet ensuite de la croiser avec d'autres sources, mais aussi de l'historiser, sachant que Google ne nous donne accès qu'à 16 mois glissant d'historique.

Dans cet article, nous allons voir comment requêter l'API de Google Search Console, afin de stocker la donnée dans Google BigQuery. Ce code permet de le faire pour plusieurs propriétés en même temps, ce qui est un gain de temps important.

Il s'agit aussi d'un prétexte pour apprendre à se connecter à une API, et à déverser la donnée dans BigQuery

### Pré-requis

- Avoir les accès "propriétaire" à au moins une propriété *Google Search Console*.
- Avoir un compte Google Cloud Platform (ou en créer un).
- Connaissances de base dans Google BigQuery
- Quelques connaissances de base en programmation Python

**Nous allons couvrir les sujets suivant :**

- Créer un "Service account user" dans Google Cloud platform, et activer les droits et accès
- Préparer l'environnement Python
- Adapter et faire tourner le code
- Lire les résultats

## Etape 1 : créer l'environnement dans Big Query

### Créer un projet dans GCP et activer l'API Search Console

Créez un projet dans Google Cloud Platform.

Ensuite, activez les APIs Google Search Console. Pour cela, accéder à la librairie des APIs [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)

Chercher la "Search console API LEGACY", et activez la si ce n'est pas déjà fait

### Créer un "service account" dans GCP

Dans GCP, aller dans "IAM & Admin" → Service accounts ([https://console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts))

- Cliquer sur "Create service account
- Créer le compte
- Lui donner un rôle qui permette l'écriture et la création de tables dans BigQuery (Admin)
- Créer une clé pour ce compte (JSON). Cette clé est téléchargée sur votre ordinateur. Nous en aurons besoin par la suite.

### Dans BigQuery, créer un dataset

Pour notre exemple, nous le nommerons "search_console_demo"

### Donner accès à ce compte dans Google Search Console

Dans Google Search console, donner un accès à ce compte pour chacune des propriétés que vous souhaitez exporter

## Etape 2 : le code Python

### Copier les fichiers nécessaires

Copier les fichiers search_console_bq.py et requirements.txt sur votre ordinateur, ainsi que la clé json générée.

### Modifier la config

Dans le début du fichier search_console_bq.py :

```python
########### SET YOUR PARAMETERS HERE ####################################
PROPERTIES = ["https://www.site1.com","https://site2.com"]
BQ_DATASET_NAME = 'search_console_demo'
BQ_TABLE_NAME = 'your_table_name'
SERVICE_ACCOUNT_FILE = 'your_key_file.json'
start_date = '2020-08-01'
end_date = '2020-08-20'
################ END OF PARAMETERS ######################################
```

### Installer les packages Python nécessaires

Dans le terminal :

- Créer un environnement virtuel :

```bash
python3 -m venv env                   
source env/bin/activate
```

- Installer les packages nécessaires :

```bash
pip install -r requirements.txt
```

Pour info, voici les packages en question :

```python
google-api-python-client==1.10.0
google-auth-httplib2==0.0.4
google-auth-oauthlib==0.4.1
google-cloud==0.34.0
google-cloud-bigquery==1.25.0
pandas==1.0.5
requests==2.22.0
pyarrow==1.0.1
```

### Lancer le script

```bash
python search_console_bq.py
```

Et voilà ;-) Si tout va bien, les données sont requêtées et chargées dans BigQuery

## Prochaines étapes

Nous verrons par la suite comment :

- Déployer le code dans Google Cloud App Engine
- Lancer une tache journalière pour mettre à jour les données

Nous verrons cela dans l'article suivant : [Tutoriel : débuter avec Google App Engine](https://www.unnest.co/dossiers/tutoriel-deployer-une-application-python-avec-google-app-engine/) 
