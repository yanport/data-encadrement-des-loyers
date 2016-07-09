# Données brutes OLAP et DRIHL de l'encadrement des loyers
Parce que l'Etat et/ou observatoires ne sont pas capables ou ne veulent pas publier correctement leurs données.

Les données 2015 et 2016 de l'encadrement des loyers à Paris disponibles sur le site de la DRIHL sont compilées dans un [fichier CSV](data/encadrement_loyers_paris.csv).

Les données 2015 de l'OLAP sont disponibles dans un [fichier json](data/2015_olap_medians.json). L'OLAP n'a rien publié pour 2016.

Ces données sont redistribuées sous la licence OpenData [ODBL](http://www.vvlibri.org/fr/licence/odbl/10/fr/legalcode).

Réferences :
 - OLAP : http://www.observatoire-des-loyers.fr/
 - DRIHL : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/le-dispositif-d-encadrement-des-loyers-a-paris-a3564.html
 - Arrêté préfectoral 2015 : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/Arrete_no2015_176_-_0007_cle5d1377.pdf
 - Arrêté préfectoral 2016 : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/recueil-idf-033-2016-06-raa-special-pdf_cle076ba9.pdf


NB : les géométries des quartiers de Paris sont disponibles sur le portail de l'APUR : http://cassini.apur.opendata.arcgis.com/datasets/12f1272266204fbe951d8e9d172c7826_0

# Install sous python3
```
pip install -r requirements.txt
apt-get install pdftohtml
```

# Générer les données soi-même sous python 3
```
python scripts/make_encadrement_csv.py data/encadrement_loyers_paris.csv
. scripts/make_olap_json.sh
```
