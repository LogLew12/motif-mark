#!/usr/bin/env python
import cairo
import argparse
import re

# getting arguments
def get_args():
    parser = argparse.ArgumentParser(
        description="Takes a file of motifs and a fasta file with lower case letters as introns and upper case characters as exons. Returns figures with exons as rectangles and lines as introns, with colored sections as motifs"
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
    "W": "[A|T]",
    "Y": "[C|T]",
    "S": "[C|G]",
    "M": "[A|C]",
    "K": "[G|T]",
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
    def __init__(self, whole):
        """Sequence object from fasta file"""
        self.whole = whole
        self.exon = []
        self.intron = []
        self.motif_loc = {}

    def split_ex_in(self):
        """Takes a sequence and populate the introns and
        exon attributes based on upper and lower case letters"""
        self.exon = re.findall("[A-Z]+", self.whole)
        self.intron = re.findall("[a-z]+", self.whole)


test_motif = Motif("YYTG", [0.5, 0.5, 0.5])
test_motif.create_regex()
print(test_motif.regex)

test_seq = Sequence("actgtGCATAGgctgaa")
test_seq.split_ex_in()
print(test_seq.exon)
print(test_seq.intron)
