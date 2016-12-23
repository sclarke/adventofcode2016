import re
from functools import partial, lru_cache

import numpy as np
import pandas as pd

with open('d22.txt') as f:
    nodes = pd.read_fwf(f, widths=[22, 6, 6, 7, 6])

nodes.rename(columns={'Use%': 'UsePercent'}, inplace=True)
nodes = nodes.applymap(lambda s: s.replace('T', 'e12').replace('%', 'e-2'))

nodes = pd.concat([nodes, nodes.Filesystem.str.extract(r'x(?P<x>\d+)-y(?P<y>\d+)', expand=True).astype('int')], axis=1)
nodes = nodes.drop(labels='Filesystem', axis=1)

nodes[['Size', 'Used', 'Avail', 'UsePercent']] = nodes[['Size', 'Used', 'Avail', 'UsePercent']].applymap(np.float)


def find_pairs(row, df):
    if row.Used == 0:
        return 0
    pair_series = row.Used <= df.Avail
    pair_series.loc[row.name] = False  # ignore the current row
    return pair_series.sum()

# find_pairs_in_nodes = partial(find_pairs, df=nodes)
# pair_series = nodes.apply(find_pairs_in_nodes, axis=1)
# print('Part 1: {}'.format(pair_series.sum()))


def parse_rows(row, df):

    # def dist(r1, r2):
    #     return abs(r1.x - r2.x) + abs(r1.y - r2.y)

    # neighbor_sizes = [r2.Size for i, r2 in df.iterrows() if dist(row, r2) == 1]

    if (row.x, row.y) == (df.x.max(), 0):
        return 'G'
    elif row.Used == 0:
        return ' '
    elif row.Used > 1e14:  # by inspection
        return '#'
    else:
        return '•'


def visualize_nodes(df):
    parser = partial(parse_rows, df=df)
    markers = df.apply(parser, axis=1)._set_name('m')
    vis_df = pd.concat([df[['x', 'y']], markers], axis=1)
    vis_df = vis_df.pivot(index='y', columns='x')

    return vis_df


vis_df = visualize_nodes(nodes)
print(vis_df.to_string())
