# usage: python downloadGigaPan.py <photo-id> <start-height> <start-width>
# http://gigapan.org/gigapans/<photo-id>

import sys
import os
import math
import shutil
import requests

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


def d(i, j, s):
    filename = "%04d-%04d.jpg" % (i, j)
    url = "%s/get_ge_tile/%d/%d/%d/%d" % (
        base, photo_id, maxlevel, j, i
    )

    print(url, filename)
    sys.stdout.flush()

    try:
        h = s.get(url, stream=True)
    except requests.exceptions.ConnectionError as e:
        # Needs improvement
        print(
            'Failed to download width:{}  height:{}. Retry with new session!'
            .format(i, j)
        )
        sys.stdout.flush()
        with requests.Session() as s:
            h = s.get(url, stream=True)

    with open('downloads/{}/{}'.format(photo_id, filename), 'wb') as f:
        shutil.copyfileobj(h.raw, f)


# main

photo_id = int(sys.argv[1])
if not os.path.exists(str(photo_id)):
    os.makedirs(str(photo_id))

base = 'http://www.gigapan.org'

# read the kml file
h = requests.get('{}/gigapans/{}.kml'.format(base, photo_id))
dom = parseString(h.text)

arglen = len(sys.argv)
start_height = int(sys.argv[2]) if arglen >= 3 else 0
start_width = int(sys.argv[3]) if arglen >= 4 else 0

# find the width and height, level
height = int(find_element_value(dom.documentElement, 'maxHeight'))
width = int(find_element_value(dom.documentElement, 'maxWidth'))
tile_size = int(find_element_value(dom.documentElement, 'tileSize'))
print(width, height, tile_size, start_width, start_height)

maxlevel = max(math.ceil(width/tile_size), math.ceil(height/tile_size))
maxlevel = int(math.ceil(math.log(maxlevel) / math.log(2.0)))
wt = int(math.ceil(width/tile_size)) + 1
ht = int(math.ceil(height/tile_size)) + 1
print(ht, wt, maxlevel)

# loop around to get every tile
for j in range(start_height, ht):
    with requests.Session() as s:
        try:
            with Pool(processes=4) as pool:
                pool.starmap(
                    d, zip(range(start_width, wt), repeat(j), repeat(s))
                )
        except requests.exceptions.ConnectionError as e:
            pass
    with open('last.txt', 'w') as f:
        f.write('height: {}'.format(j))
