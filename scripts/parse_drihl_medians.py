# -*- coding: utf-8 -*-

import sys
import csv
import io
import requests
import xml.etree.ElementTree as ET
import itertools

from enum import Enum


class Period(Enum):
    before_1946 = 'inf1946'
    between_1946_1970 = '1946-1970'
    between_1971_1990 = '1971-1990'
    after_1990 = 'sup1990'


def build_drihl_url(year, room_count, period, furnished):
    assert room_count in range(1, 5)
    assert year in [2015, 2016]

    date = '2016-08-01' if year == 2016 else '2015-08-01'
    furnished = 'meuble' if furnished else 'non-meuble'

    return 'http://www.referenceloyer.drihl.ile-de-france.developpement-durable.gouv.fr/kml/%s/drihl_medianes_%s_%s_%s.kml?t=20150327' % (date, room_count, period.value, furnished)


def parse_kml(response, year):
    kml = ET.fromstring(response.text.replace(' xmlns="http://earth.google.com/kml/2.1"', ''))

    document = kml.getchildren()[0]

    parsed_data = []

    for extended_data in document.findall('.//Placemark/ExtendedData'):
        element = {}
        for data in extended_data.getchildren():
            attr_name = data.attrib['name']

            if attr_name in ['ref', 'refmaj', 'refmin']:
                element['%s_%s' %(attr_name, year)] = round(float(data.findtext('value').replace(',', '.')), 1)
            else:
                element[attr_name] = data.findtext('value')

        parsed_data.append(element)

    return parsed_data


def fetch_and_parse_kml():
    output = []
    total = 4 * 4 * 2 * 2
    print("#{0} pages to download".format(total))

    count = 0
    for room_count, period, furnished in itertools.product(range(1, 5), Period, [False, True]):
        results_by_year = []
        for year in [2015, 2016]:
            count += 1
            url = build_drihl_url(year, room_count, period, furnished)

            print ("download url {0} - {1}/{2}".format(url, count, total))

            response = requests.get(url)

            results_by_year.append(parse_kml(response, year))

        for row_2015, row_2016 in zip(results_by_year[0], results_by_year[1]):
            row_2015.update(row_2016)

        output += results_by_year[0]

    return output


if __name__ == '__main__':
    output_file = sys.argv[1]

    with io.open(output_file, 'w', encoding='utf8') as csvfile:
        data = fetch_and_parse_kml()

        writer = csv.DictWriter(csvfile, fieldnames=['idZone', 'nameZone', 'idQuartier', 'piece', 'epoque', 'type', 'ref_2015', 'ref_2016', 'refmin_2015', 'refmin_2016', 'refmaj_2015', 'refmaj_2016'])
        writer.writeheader()
        writer.writerows(data)
