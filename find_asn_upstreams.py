#!/usr/bin/env python

import bz2
import urllib
from collections import defaultdict

def uniqlist(items):
	s = list()
	for i in items:
		if i not in s:
			s.append(i)
	return s


latest_file_url = 'http://archive.routeviews.org/oix-route-views/oix-full-snapshot-latest.dat.bz2'
route_file = 'oix-full-snapshot-latest.dat.bz2'
csv_file = 'asn_peers.csv'

print "Downloading file, please wait..."
u = urllib.urlretrieve(latest_file_url, route_file)

data = defaultdict(list)
print "Parsing file for as paths..."
with bz2.BZ2File(route_file, 'rb') as rf:
	for line in rf:
		if line.startswith('*') and '{' not in line:
			path = line.split()[6:-1]
			path = uniqlist(path)
			if len(path) > 1:
				data[path[-1]].append(path[-2])

print "Cleaning up the data..."
pairs = dict()
for source, peers in data.items():
	pairs[source] = list(set(peers))

print "Writing output..."
with open(csv_file, 'w') as cvf:
	header =  "source_asn, number_of_peers, peer_list\n"
	cvf.write(header)
	for source, peers in pairs.items():
		numpeers = str(len(peers))
		line = source + ',' + numpeers + ',' +  ','.join(peers) + '\n'
		cvf.write(line)

print "Done!, results written to:", csv_file
