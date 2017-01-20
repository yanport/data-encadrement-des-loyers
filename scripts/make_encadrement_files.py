# -*- coding: utf-8 -*-

import copy
import csv
import html
import io
import itertools
import json
import requests
import sys

from enum import Enum

URL = 'http://preprod.www.encadrementloyers.com.wdf-01.ovea.com/'
HEADERS = {'X-Requested-With': 'XMLHttpRequest'}


class City(Enum):
    PARIS = 1
    LILLE = 2

# ID coming from https://www.insee.fr/fr/statistiques/fichier/2017499/IRIS_table_geo2015.zip
PARIS_QUARTER_IDS = [
    "7510101",
    "7510102",
    "7510103",
    "7510104",
    "7510205",
    "7510206",
    "7510207",
    "7510208",
    "7510309",
    "7510310",
    "7510311",
    "7510312",
    "7510413",
    "7510414",
    "7510415",
    "7510416",
    "7510517",
    "7510518",
    "7510519",
    "7510520",
    "7510621",
    "7510622",
    "7510623",
    "7510624",
    "7510725",
    "7510726",
    "7510727",
    "7510728",
    "7510829",
    "7510830",
    "7510831",
    "7510832",
    "7510933",
    "7510934",
    "7510935",
    "7510936",
    "7511037",
    "7511038",
    "7511039",
    "7511040",
    "7511141",
    "7511142",
    "7511143",
    "7511144",
    "7511245",
    "7511246",
    "7511247",
    "7511248",
    "7511349",
    "7511350",
    "7511351",
    "7511352",
    "7511453",
    "7511454",
    "7511455",
    "7511456",
    "7511557",
    "7511558",
    "7511559",
    "7511560",
    "7511661",
    "7511662",
    "7511663",
    "7511664",
    "7511765",
    "7511766",
    "7511767",
    "7511768",
    "7511869",
    "7511870",
    "7511871",
    "7511872",
    "7511973",
    "7511974",
    "7511975",
    "7511976",
    "7512077",
    "7512078",
    "7512079",
    "7512080",
]

LILLE_IRIS_IDS = [
    "593500101",
    "593500104",
    "593500105",
    "593500106",
    "593500107",
    "593500108",
    "593500109",
    "593500110",
    "593500111",
    "593500112",
    "593500113",
    "593500114",
    "593500115",
    "593500116",
    "593500117",
    "593500118",
    "593500119",
    "593500201",
    "593500202",
    "593500203",
    "593500204",
    "593500205",
    "593500206",
    "593500207",
    "593500302",
    "593500303",
    "593500304",
    "593500305",
    "593500306",
    "593500307",
    "593500308",
    "593500309",
    "593500310",
    "593500401",
    "593500402",
    "593500403",
    "593500404",
    "593500405",
    "593500406",
    "593500407",
    "593500408",
    "593500409",
    "593500410",
    "593500501",
    "593500502",
    "593500503",
    "593500504",
    "593500506",
    "593500507",
    "593500508",
    "593500601",
    "593500602",
    "593500603",
    "593500604",
    "593500701",
    "593500702",
    "593500703",
    "593500704",
    "593500705",
    "593500706",
    "593500707",
    "593500709",
    "593500710",
    "593500711",
    "593500801",
    "593500802",
    "593500803",
    "593500804",
    "593500901",
    "593500902",
    "593500903",
    "593500904",
    "593500905",
    "593500906",
    "593500907",
    "593500908",
    "593501001",
    "593501002",
    "593501003",
    "593501004",
    "593501005",
    "593501006",
    "593501007",
    "593501008",
    "593502401",
    "593502402",
    "593502403",
    "593502404",
    "593502405",
    "593502501",
    "593502502",
    "593502503",
    "593502601",
    "593502602",
    "593502603",
    "593502701",
    "593502702",
    "593502703",
    "593502704",
    "593502705",
    "593502706",
    "593502801",
    "593502802",
    "593502901",
    "593502902",
    "593502903",
    "593502904",
    "593503001",
    "593503002",
    "593503003",
]

PERIODS = ['Avant 1946', '1946-1970', '1971-1990', 'Apres 1990']
ROOM_COUNTS = [1, 2, 3, 4]


def get_encadrement(data):
    result = requests.post(URL, headers=HEADERS, data=data).json()

    assert result['data']['found']
    return result['data']['prix']


def get_quarters(city):
    result = requests.post(URL, headers=HEADERS, data={'ville': city.value, 'td': 'getQuartiers'}).json()
    return result['data']


def get_iris_code(ville, id_quartier):
    # The "quarters" are coming from iris grand quartier for Paris and iris for Lille
    if ville == 'PARIS':
        return

    if ville == 'LILLE':
        # the id starts at 81 and has no relation with iris id but the order is the same as in the file
        # https://www.insee.fr/fr/statistiques/fichier/2017499/IRIS_table_geo2015.zip
        return LILLE_IRIS_IDS[int(id_quartier) - 81]


def get_grand_quartier_code(ville, id_quartier):
    if ville == 'PARIS':
        return next(filter(lambda q: q[-len(id_quartier):] == id_quartier, PARIS_QUARTER_IDS))

    if ville == 'LILLE':
        return get_iris_code(ville, id_quartier)[:7]


def fetch_encadrement():
    data = []

    for city in City:
        quarters = get_quarters(city)

        for quarter in quarters:
            quarter['name'] = html.unescape(quarter['name'])

        dates = [2017]

        if city == City.PARIS:
            dates = [2015, 2016]

        for (quarter, room_count, period, furnished, date) in itertools.product(quarters, ROOM_COUNTS, PERIODS, [0, 1], dates):
            print(quarter['name'], period, room_count, date, furnished)

            request_data = {
                'secteur': quarter['secteur'],
                'ville': city.value,
                'epoque': period,
                'date': date,
                'meuble': furnished,
                'piece': room_count,
            }

            result = get_encadrement(request_data)
            request_data.update(result)
            request_data['quarter'] = quarter
            request_data['ville'] = city.name

            data.append(request_data)

    return data


def write_csv(data, filename):
    with io.open(filename + '.csv', 'w', encoding='utf8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['ville', 'id_zone', 'code_grand_quartier', 'code_iris', 'nom_quartier', 'piece', 'epoque', 'meuble', 'annee', 'ref', 'min', 'max'])
        writer.writeheader()

        for row in data:
            row = copy.deepcopy(row)
            quarter = row.pop('quarter')
            row['id_zone'] = row.pop('secteur')
            row['code_grand_quartier'] = get_grand_quartier_code(row['ville'], quarter['id'])
            row['code_iris'] = get_iris_code(row['ville'], quarter['id'])
            row['nom_quartier'] = quarter['name']
            row['annee'] = row.pop('date')
            writer.writerow(row)


def write_geojson(data, filename):
    geojson = {"type": "FeatureCollection", "features": []}

    with io.open(filename + '.geojson', 'w', encoding='utf-8') as json_file:
        for key, group in itertools.groupby(data, lambda r: r['quarter']['id']):
            group = list(group)
            quarter = group[0]['quarter']
            coordinates = [
                [[c[1], c[0]] for c in quarter['polygon']]
            ]

            elements = []
            for element in group:
                element = copy.deepcopy(element)
                element.pop('quarter')
                element['id_zone'] = element.pop('secteur')
                element['code_grand_quartier'] = get_grand_quartier_code(element['ville'], quarter['id'])
                element['code_iris'] = get_iris_code(element['ville'], quarter['id'])
                element['nom_quartier'] = quarter['name']
                element['annee'] = element.pop('date')
                elements.append(element)

            feature = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": coordinates}, 'properties': elements}

            geojson["features"].append(feature)

        json.dump(geojson, json_file, indent=2)


if __name__ == '__main__':
    output_filename = sys.argv[1]

    data = fetch_encadrement()
    write_csv(data, output_filename)
    write_geojson(data, output_filename)
