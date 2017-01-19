# -*- coding: utf-8 -*-

import sys
import csv
import io
import copy
import json
import requests
import itertools

from enum import Enum

URL = 'http://preprod.www.encadrementloyers.com.wdf-01.ovea.com/'
HEADERS = {'X-Requested-With': 'XMLHttpRequest'}


class City(Enum):
    PARIS = 1
    LILLE = 2


PERIODS = ['Avant 1946', '1946-1970', '1971-1990', 'Apres 1990']
ROOM_COUNTS = [1, 2, 3, 4]


REQUEST_DATA = {
    'epoque': 'Apres 1990',
    'ville': 1,
    'date': 2017,
    'meuble': 0,
    'piece': 2,
    'secteur': 13,
    'date': 2015
}


def get_encadrement(data):
    result = requests.post(URL, headers=HEADERS, data=data).json()

    assert result['data']['found']
    return result['data']['prix']


def get_quarters(city):
    result = requests.post(URL, headers=HEADERS, data={'ville': city.value, 'td': 'getQuartiers'}).json()
    return result['data']


def fetch_encadrement():
    data = []

    for city in City:
        quarters = get_quarters(city)

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
        writer = csv.DictWriter(csv_file, fieldnames=['ville', 'id_zone', 'id_quartier', 'nom_quartier', 'piece', 'epoque', 'meuble', 'annee', 'ref', 'min', 'max'])
        writer.writeheader()

        for row in data:
            row = copy.deepcopy(row)
            quarter = row.pop('quarter')
            row['id_zone'] = row.pop('secteur')
            row['id_quartier'] = quarter['id']
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
                element['id_quartier'] = quarter['id']
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
