# Données brutes OLAP et DRIHL de l'encadrement des loyers
Parce que l'Etat et/ou observatoires ne sont pas capables ou ne veulent pas publier correctement leurs données.

Les données 2015 et 2016 de l'encadrement des loyers à Paris sont compilées dans un [fichier CSV](data/encadrement_loyers_paris.csv).

Ces données sont redistribuées sous la licence OpenData [ODBL](http://www.vvlibri.org/fr/licence/odbl/10/fr/legalcode).

Réferences :
 - OLAP : http://www.observatoire-des-loyers.fr/
 - DRIHL : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/le-dispositif-d-encadrement-des-loyers-a-paris-a3564.html


# Install
```
pip install -r requirements.txt
apt-get install pdftohtml
```

# Générer les données soi-même
```
python scripts/parse_drihl_medians.py data/encadrement_loyers_paris.csv
. scripts/make_olap_json.sh
```
