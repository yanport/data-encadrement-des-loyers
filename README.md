# Données brutes OLAP et DRIHL de l'encadrement des loyers
Parce que l'Etat et/ou observatoires ne sont pas capables ou ne veulent pas publier correctement leurs données.

Réferences :
 - OLAP : http://www.observatoire-des-loyers.fr/
 - DRIHL : http://www.drihl.ile-de-france.developpement-durable.gouv.fr/le-dispositif-d-encadrement-des-loyers-a-paris-a3564.html

# Install
pip install -r requirements.txt
apt-get install pdftohtml

# Générer les données soi-mêmes
```
. scripts/make_drihl_json.sh
. scripts/make_olap_json.sh
```
