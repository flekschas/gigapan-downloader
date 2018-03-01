#!/usr/bin/env python3

import json
import sys

arglen = len(sys.argv)
snap1_path = sys.argv[1] if arglen >= 1 else 0
snap2_path = sys.argv[2] if arglen >= 2 else 0

if not snap1_path or not snap2_path:
    print('2 snapshot files need to be provided.')
    sys.exit(1)

with open(snap1_path, 'r') as f1:
    with open(snap2_path, 'r') as f2:
        snap1 = json.load(f1)
        snap2 = json.load(f2)

if not snap1 or not snap2:
    print('Something broke. Ciao.')
    sys.exit(1)

total_views_snap1 = 0
total_views_snap2 = 0

for snap in snap1:
    total_views_snap1 += snap['snapshot']['views']

for snap in snap2:
    total_views_snap2 += snap['snapshot']['views']

snap1_id_to_snap = {}
snap2_id_to_snap = {}

for ind, snap in enumerate(snap1):
    snap1_id_to_snap[snap['snapshot']['id']] = snap['snapshot']
    snap['snapshot']['views_original'] = snap['snapshot']['views']
    snap['snapshot']['views'] /= total_views_snap1

for snap in snap2:
    snap2_id_to_snap[snap['snapshot']['id']] = snap['snapshot']
    snap['snapshot']['views_original'] = snap['snapshot']['views']
    snap['snapshot']['views'] /= total_views_snap2

new_snap = snap1 + snap2

# Search for duplictaes
delete = []
for ind, snap in enumerate(new_snap):
    if 'duplicate' in snap['snapshot']:
        src = snap1_id_to_snap[snap['snapshot']['src_id']]
        src['views'] = (
            (src['views_original'] + snap['snapshot']['views_original']) /
            (total_views_snap1 + total_views_snap2)
        )
        delete.append(ind)

for ind in delete:
    del new_snap[ind]


with open('combined.json', 'w') as f:
    json.dump(new_snap, f)
