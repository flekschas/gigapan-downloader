#!/usr/bin/env python3

# usage: python downloadGigaPan.py <photo-id> <start-height> <start-width>
# http://gigapan.org/gigapans/<photo-id>

import sys
import os
import math
import shutil
import requests
import json
import pathlib

from multiprocessing import Pool
from xml.dom.minidom import parseString
from itertools import repeat


def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc


def find_element_value(e, name):
    nodelist = [e]
    while len(nodelist) > 0:
        node = nodelist.pop()
        if node.nodeType == node.ELEMENT_NODE and node.localName == name:
            return getText(node.childNodes)
        else:
            nodelist += node.childNodes

    return None


def d(i, j, z, s):
    filename = "%d.%d.%d.jpg" % (z, j, i)
    url = "%s/get_ge_tile/%d/%d/%d/%d" % (
        base, photo_id, z, j, i
    )

    tile = 'downloads/{}/tiles/{}'.format(photo_id, filename)
    downloaded = False

    if (
        not os.path.isfile(tile) or
        os.path.getsize(tile) == 0
    ):
        try:
            r = s.get(url, stream=True)
        except requests.exceptions.ConnectionError as e:
            # Needs improvement
            print(
                'Failed to download zoom:{} width:{}  height:{}. Retry!'
                .format(z, i, j)
            )
            sys.stdout.flush()
            with requests.Session() as s:
                r = s.get(url, stream=True)

        if r.status_code == 200:
            with open(tile, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            downloaded = True

    print(url, filename, 'downloaded' if downloaded else 'skipped')
    sys.stdout.flush()


# main

photo_id = int(sys.argv[1])
if not os.path.exists(str(photo_id)):
    os.makedirs(str(photo_id))

base = 'http://www.gigapan.org'

# read the kml file
r = requests.get('{}/gigapans/{}.kml'.format(base, photo_id))
dom = parseString(r.text)

arglen = len(sys.argv)
start_height = int(sys.argv[2]) if arglen >= 3 else 0
start_width = int(sys.argv[3]) if arglen >= 4 else 0
start_zoom = int(sys.argv[4]) if arglen >= 5 else 0

# find the width and height, level
height = int(find_element_value(dom.documentElement, 'maxHeight'))
width = int(find_element_value(dom.documentElement, 'maxWidth'))
tile_size = int(find_element_value(dom.documentElement, 'tileSize'))

max_zoom = max(math.ceil(width/tile_size), math.ceil(height/tile_size))
max_zoom = int(math.ceil(math.log(max_zoom) / math.log(2.0)))
print(width, height, tile_size, start_width, start_height, max_zoom)

pathlib.Path(
    'downloads/{}/tiles'.format(photo_id)
).mkdir(parents=True, exist_ok=True)

# Get annotations
r = requests.get('{}/gigapans/{}/snapshots.json'.format(base, photo_id))
with open('downloads/{}/snapshots.json'.format(photo_id), 'w') as f:
    f.write(r.text)

# Write tile set infos
with open('downloads/{}/info.json'.format(photo_id), 'w') as f:
    json.dump({
        "tile_size": tile_size,
        "max_width": width,
        "max_height": height,
        "max_zoom": max_zoom
    }, f)

# loop over all zoom levels
for z in range(start_zoom, max_zoom + 1):
    div = 2 ** (max_zoom - z)
    wt = int(math.ceil((width / div) / tile_size))
    ht = int(math.ceil((height / div) / tile_size))
    print(z, wt, ht)
    for j in range(start_height, ht):
        with requests.Session() as s:
            try:
                with Pool(processes=4) as pool:
                    pool.starmap(
                        d,
                        zip(
                            range(start_width, wt),
                            repeat(j),
                            repeat(z),
                            repeat(s)
                        )
                    )
            except requests.exceptions.ConnectionError as e:
                pass
        with open('last.txt', 'w') as f:
            f.write('zoom: {}; height: {}'.format(z, j))
