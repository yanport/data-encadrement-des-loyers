# Données brutes [OLAP](http://www.observatoire-des-loyers.fr/) et du [Ministère du logement](http://www.logement.gouv.fr/) de l'encadrement des loyers
Parce que l'Etat et/ou observatoires ne sont pas capables ou ne veulent pas publier correctement leurs données.

Depuis 2016, Le Ministère du logement a mis en ligne un site pour permettre à chacun de savoir si un loyer est compris dans l'encadrement. C'est une très bonne initiative mais toujours pas de données en #OpenData. 

Vous trouverez ici les données 2015 et 2016 de l'encadrement des loyers à Paris et à Lille extraite du site http://www.encadrementdesloyers.gouv.fr/ et compilées dans un [fichier CSV](data/encadrement_loyers.csv) et un [fichier geojson](data/encadrement_loyers.geojson)

Vous trouverez également les données 2015 de l'OLAP sont disponibles dans un [fichier json](data/2015_olap_medians.json). L'OLAP n'a rien publié pour 2016.

Ces données sont redistribuées sous la licence OpenData [ODBL](http://www.vvlibri.org/fr/licence/odbl/10/fr/legalcode).

Réferences :
 - OLAP : http://www.observatoire-des-loyers.fr/
 - Site de l'encadrement des loyers : http://www.encadrementdesloyers.gouv.fr/
 - Arrêté préfectoral 2015 - Paris : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/Arrete_no2015_176_-_0007_cle5d1377.pdf
 - Arrêté préfectoral 2016 - Paris : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/recueil-idf-033-2016-06-raa-special-pdf_cle076ba9.pdf
  - Arrêté préfectoral 2016 - Lille : http://nord.gouv.fr/content/download/39271/272349/file/161216_arrete_encadrement_des_loyers_lille.pdf


NB : les géométries des quartiers de Paris sont aussi disponibles sur le portail de l'APUR : http://cassini.apur.opendata.arcgis.com/datasets/12f1272266204fbe951d8e9d172c7826_0

# Install sous python3
```
pip install -r requirements.txt
apt-get install pdftohtml
```

# Générer les données soi-même sous python 3
```
python scripts/make_encadrement_files.py data/encadrement_loyers
. scripts/make_olap_json.sh
```
