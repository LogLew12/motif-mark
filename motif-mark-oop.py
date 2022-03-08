#!/usr/bin/env python
import cairo
import argparse
import re

# getting arguments
def get_args():
    parser = argparse.ArgumentParser(
        description="Takes a file of motifs and a fasta file with lower case letters as introns and upper scase characters as exons. Returns figures with exons as rectangles and lines as introns, with colored sections as motifs"
    )
    parser.add_argument(
        "-f",
        "--file",
        help="input fasta with upper case exons and lower case introns",
        required=True,
    )
    parser.add_argument(
        "-m", "--motifs", help="input file with one motif on each line", required=True
    )
    return parser.parse_args()


args = get_args()

regex_dict = {
    "A": "A",
    "C": "C",
    "G": "G",
    "T": "T",
    "U": "T",
    "W": "[A|T]",
    "Y": "[C|T]",
    "S": "[C|G]",
    "M": "[A|C]",
    "K": "[G|T|U]",
    "R": "[A|G]",
    "B": "[C|G|T]",
    "D": "[A|G|T]",
    "H": "[A|C|T]",
    "V": "[A|C|G]",
    "N": "[A|C|G|T]",
}


class Motif:
    def __init__(self, whole, color):
        """Motif sequence object"""
        self.whole = whole
        self.color = color
        self.regex = ""

    def create_regex(self):
        """creates regex string to find patterns that match the motif"""
        for i in self.whole:
            self.regex = self.regex + regex_dict[i]


class Sequence:
    def __init__(self, whole, header):
        """Sequence object from fasta file"""
        self.whole = whole
        self.header = header
        self.exon = []
        self.intron = []
        self.motif_loc = {}

    def split_ex_in(self):
        """Takes a sequence and populate the introns and
        exon attributes based on upper and lower case letters"""
        self.exon = re.findall("[A-Z]+", self.whole)
        self.intron = re.findall("[a-z]+", self.whole)

    def find_motifs(self, motif_list):
        """Takes a list of motifs and populates a dictionary
        with motifs as keys and their positions in the sequence as values"""
        for motif in motif_list:
            pos_list = []
            for x in re.finditer(motif.regex, self.whole.upper()):
                pos_list.append(x.span())
            self.motif_loc[motif] = pos_list


Motif_list = []
with open(args.motifs) as fh_m:
    for line in fh_m:
        line = line.strip()
        Motif_list.append(Motif(line.upper(), [0.5, 0.5, 0.5]))

for obj in Motif_list:
    obj.create_regex()

Sequence_list = []
with open(args.file) as fh:
    header = ""
    seq_storage = ""
    for line in fh:
        line = line.strip()
        if line.startswith(">") and header == "":
            header = line
        elif line.startswith(">"):
            Sequence_list.append(Sequence(seq_storage, header))
            header = line
            seq_storage = ""
        else:
            seq_storage = seq_storage + line
    Sequence_list.append(Sequence(seq_storage, header))

lengths = []
for seq in Sequence_list:
    seq.split_ex_in()
    seq.find_motifs(Motif_list)
    lengths.append(len(seq.whole))

# drawing
# Creating the cairo surface
HEIGHT = 300 * len(Sequence_list)
WIDTH = max(lengths) + 100
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# Setting a background color
ctx.save()
ctx.set_source_rgb(1.0, 1.0, 1.0)
ctx.paint()
ctx.restore()


for i, seq in enumerate(Sequence_list):
    # drawing line
    line_col = "black"
    h = 150 + (300 * i)
    ctx.set_line_width(5)
    ctx.move_to(50, h)
    ctx.line_to(len(seq.whole) + 50, h)
    ctx.stroke()

    # drawing rectangle
    ctx.rectangle(
        50 + len(seq.intron[0]), h - 30, len(seq.exon[0]), 60
    )  # Rectangle(x0, y0, x1, y1)
    ctx.fill()


# saving png
surface.write_to_png("test1.png")
