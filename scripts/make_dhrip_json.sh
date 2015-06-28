#!/bin/bash
# USAGE: ./scripts/make_dhrip_json.sh

mkdir data/tmp

python scripts/parse_dhrip_medians.py data/2015_dhrip_medians.json

rm -r data/tmp