# -*- coding: utf-8 -*-

import io
import sys
import json
import requests
import xml.etree.ElementTree as ET

BASE_URL = 'https://www.referidf.com/kml'


def parse_kml(response):
    kml = ET.fromstring(response.content.decode('utf-8').replace(' xmlns="http://earth.google.com/kml/2.1"', ''))

    document = kml.getchildren()[0]

    parsed_data = []

    for extended_data in document.findall('.//Placemark/ExtendedData'):
        element = {}
        for data in extended_data.getchildren():
            attr_name = data.attrib['name']

            if attr_name in ['ref', 'refmaj', 'refmin']:
                element[attr_name] = float(data.findtext('value').replace(',', '.'))
            else:
                element[attr_name] = data.findtext('value')


        parsed_data.append(element)

    return parsed_data


def fetch_and_parse_kml():
    output = []

    total = 4 * 4 * 2
    print("#{0} pages to download".format(total))

    count = 0
    for room_count in range(1, 5):
        for period in ["inf1946", "1946-1970", "1971-1990", "sup1990"]:
            for is_furshished in ["meuble", "non-meuble"]:
                url = "%s/drihl_medianes_%s_%s_%s.kml" % (BASE_URL, room_count, period, is_furshished)

                count += 1
                print ("download url {0} - {1}/{2}".format(url, count, total))

                output += parse_kml(requests.get(url, params={"t": "20150327"}))

    return output


if __name__ == '__main__':
    output_file = sys.argv[1]

    with io.open(output_file, 'w', encoding='utf8') as f:
        json.dump(fetch_and_parse_kml(), f, indent=4, ensure_ascii=False)