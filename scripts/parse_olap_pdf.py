# -*- coding: utf-8 -*-

import sys
import json
import xml.etree.cElementTree as ET

keys = ['id', 'quarterIds', 'roomCountCategory', 'constructionPeriod', 'median', 'q1', 'q3', 'std', 'count']


def parse_xml_from_pdf(xml_file):
    left_zones = None
    min_top = None
    tree = ET.ElementTree(file=xml_file)

    zones = []
    zone_limits = []
    zone_id = None
    quarter_codes = None

    print("start parsing ugly xml")

    for page in tree.iter(tag='page'):
        page_number = page.get('number')
        print("parse page {0}/3".format(page_number))

        if page_number == '1':
            min_top = 235
            left_zones = [137]

        if page_number == '2':
            min_top = 168
            left_zones = [129, 137]

        if page_number == '3':
            min_top = 147
            left_zones = [129]

        for i, elem in enumerate(page.iter('text')):
            if int(elem.get('top')) < min_top:
                continue

            if int(elem.get('left')) < left_zones[0]:
                continue

            if int(elem.get('left')) in left_zones:
                if zone_limits:
                    zones.append([zone_id, quarter_codes, zone_limits + [limit]])

                zone_limits = []
                limit = []
                text = elem.itertext().__next__()
                if text:
                    values = text.split(' ')
                    zone_id = values[0]
                    quarter_codes = values[1:]

                continue

            if int(elem.get('left')) < left_zones[len(left_zones) - 1] + 30:
                quarter_codes += elem.itertext().__next__().split(' ')
                continue

            if len(limit) == len(keys) - 2:
                zone_limits.append(limit)
                limit = []

            text = elem.itertext().__next__()

            if len(limit) == 0:
                if text.strip() not in ['1', '2', '3', '4 et +']:
                    limit.append(zone_limits[-1][0])

            limit.append(text)

    zones.append([zone_id, quarter_codes, zone_limits + [limit]])

    json_data = []

    for row in zones:
        zone_id, quarter_codes, zone_limits = row

        for zone_limit in zone_limits:
            datum = {'zoneId': zone_id, 'quarterIds': quarter_codes}
            for key, value in zip(keys[2:], zone_limit):
                if key in ['median', 'q1', 'q3', 'std', 'count']:
                    try:
                        value = float(value.replace(',', '.'))
                    except ValueError:
                        print("error when converting to float", zone_id, quarter_codes, zone_limit)

                datum[key] = value

            json_data.append(datum)

    return json_data


if __name__ == '__main__':
    xml_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(output_file, "w") as f:
        json.dump(parse_xml_from_pdf(xml_file), f, indent=4)