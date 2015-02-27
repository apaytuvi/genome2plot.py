# genome2plot.py
The script `genome2plot.py` aims to plot a genome showing the structural variations provided. The script accepts two bed files as input:

1. A 4-column bed file `(chr, start, end, type)` providing information about the location of the structural variations. E.g. `structuralvariations.bed`.
2. A 3-column bed file `(chr, 1, end)` providing chromosome lengths. E.g. `genome.bed`.

Command:
```
genome2plot.py structuralvariations.bed genome.bed
```
The output should be something like this:
![ScreenShot](/examples/output/foo.png)
For a proper visualization, only chromosomes larger than the 5% of the largest chromosome length are displayed (thus, small scaffolds not displayed). Structural variations are represented by different colours. Colour dictionary:
```
{
"INS": "Magenta",
"DEL": "GreenYellow",
"DUP": "OrangeRed",
"INV": "SteelBlue",
"TRA": "MistyRose",
}
```