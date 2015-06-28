#!/bin/bash
# USAGE: ./scripts/make_dhrip_json.sh

mkdir data/tmp

python scripts/parse_drihl_medians.py data/2015_drihl_medians.json

rm -r data/tmp