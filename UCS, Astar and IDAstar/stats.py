'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
import collections


def map_statistics(roads):
    juncs_num = len(roads.junctions())
    links_num = sum(1 for _ in roads.iterlinks())
    avg_links = links_num / juncs_num
    links_for_junc = []
    distances = []
    for junc in roads.junctions():
        links_for_junc.append(len(junc.links))
        for link in junc.links:
            distances.append(link.distance)

    min_links = min(links_for_junc)
    max_links = max(links_for_junc)
    min_dis = min(distances)
    max_dis = max(distances)
    avg_dis = sum(distances) / len(distances)
    histogram = collections.Counter(getattr(link, 'highway_type') for link in roads.iterlinks())
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions': juncs_num,
        'Number of links': links_num,
        'Outgoing branching factor': Stat(max=max_links, min=min_links, avg=avg_links),
        'Link distance': Stat(max=max_dis, min=min_dis, avg=avg_dis),
        'Link type histogram': histogram,
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
