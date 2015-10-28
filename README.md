# Données brutes OLAP et DRIHL de l'encadrement des loyers
Parce que l'Etat et/ou observatoires ne sont pas capables ou ne veulent pas publier correctement leurs données.

Ces données sont redistribuées sous la licence OpenData [ODBL](http://www.vvlibri.org/fr/licence/odbl/10/fr/legalcode).

Réferences :
 - OLAP : http://www.observatoire-des-loyers.fr/
 - DRIHL : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/le-dispositif-d-encadrement-des-loyers-a-paris-a3564.html
 - Données fournies au format .ods (tableur) http://www.drihl.ile-de-france.developpement-durable.gouv.fr/IMG/ods/loyer_de_reference_arrete_cle22f64d.ods

# Install
```
pip install -r requirements.txt
apt-get install pdftohtml
```

# Générer les données soi-mêmes
```
. scripts/make_drihl_json.sh
. scripts/make_olap_json.sh
```
