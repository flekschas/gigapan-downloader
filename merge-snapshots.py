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

for snap in snap1:
    snap['snapshot']['views_original'] = snap['snapshot']['views']
    snap['snapshot']['views'] /= total_views_snap1

for snap in snap2:
    snap['snapshot']['views_original'] = snap['snapshot']['views']
    snap['snapshot']['views'] /= total_views_snap2

new_snap = snap1 + snap2

with open('combined.json', 'w') as f:
    json.dump(new_snap, f)
