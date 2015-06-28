#!/bin/bash
# USAGE: ./scripts/make_olap_json.sh

mkdir data/tmp

wget -O data/tmp/2015_olap_medians.pdf http://www.observatoire-des-loyers.fr/sites/default/files/olap_documents/docs_information/communication_externe/Medianes%20plus%20de%2050%20obs.pdf
pdftohtml -xml -hidden -stdout data/tmp/2015_olap_medians.pdf > data/tmp/2015_olap_medians.xml
python scripts/parse_olap_pdf.py data/tmp/2015_olap_medians.xml data/2015_olap_medians.json

rm -r data/tmp