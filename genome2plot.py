#!/usr/bin/python

import sys
import operator
from matplotlib import pyplot as plt
from matplotlib.collections import BrokenBarHCollection

variants = sys.argv[1]
genome_len = sys.argv[2]

print 'Reading genome bed file...'

file1 = open(genome_len)
lines = file1.readlines()

bed_lines = []
chrom_lens = {}
for line in lines:
    chrom, start, end = line.strip().split('\t')
    chrom_len = int(end) - int(start)
    chrom_lens[chrom] = chrom_len
    bed_lines.append((chrom, int(start), int(end), 'CHR'))

file1.close()
chrom_largest = sorted(chrom_lens.items(), key=operator.itemgetter(1), reverse = True)
largest = chrom_largest[0][1]

chrom_largest_keys = []
for inum in xrange(0, len(chrom_largest)):
    if chrom_largest[inum][1] < (chrom_largest[0][1] * 0.05):
        chrom_largest = None
        break
    chrom_largest_keys.append(chrom_largest[inum][0])

print 'Reading variants bed file...'

file2 = open(variants)
lines = file2.readlines()

for line in lines:
    chrom, start, end, typ = line.strip().split('\t')
    bed_lines.append((chrom, int(start), int(end), typ))

bed_sorted = sorted(bed_lines, key=lambda x: (x[0], x[1]))
bed_lines = None

color_lookup = {
  'DUP': 'Red',
  'DEL': 'Lime',
  'INS': 'DarkOrange',
  'INV': 'SteelBlue',
  'TRA': 'Gainsboro',
  'CHR': 'Bisque'
}

height = 0.6
spacing = 0.4

def ideograms(fn, clargest):
    xranges, colors, wid = [], [], []
    last_chrom = None
    last_start = 0
    ymin = 0
    print 'Creating plot...'
    for chrom, start, stop, label in fn:
        width = stop - start
        if chrom not in clargest:
            continue
        if chrom == last_chrom or last_chrom == None:
            xranges.append((start, width))
            colors.append(color_lookup[label])
            last_chrom = chrom
            last_start = start
            continue

        ymin += height + spacing
        yrange = (ymin, height)
        yield xranges, yrange, colors, last_chrom
        xranges, colors, wid = [], [], []
        xranges.append((start, width))
        colors.append(color_lookup[label])
        last_chrom = chrom

    ymin += height + spacing
    yrange = (ymin, height)
    yield xranges, yrange, colors, last_chrom


fig = plt.figure(figsize=(8, 0.3 * len(chrom_largest_keys)))
ax = fig.add_subplot(111)

yticks = []
yticklabels = []

for xranges, yrange, colors, chromosome in ideograms(bed_sorted, chrom_largest_keys):
    coll = BrokenBarHCollection(xranges, yrange, facecolors=colors, linewidths=0)
    ax.add_collection(coll)
    center = yrange[0] + yrange[1]/2
    yticks.append(center)
    yticklabels.append(chromosome)

ax.axis('tight')
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

xlabels = []
for xt in range(1, largest, int(largest/10)-1):
	xlabels.append('{:.2e}'.format(xt))

ax.set_xticklabels(xlabels, fontsize=6.5)
ax.set_xticks(range(1, largest, int(largest/10)-1))

fig.savefig('foo.png', dpi=400)
