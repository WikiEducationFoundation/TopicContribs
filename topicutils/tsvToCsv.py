"""tsvToCsv
Usage:
    tsvToCsv -i=<infile.tsv> -o=<outfile.csv>
    tsvToCsv (-h | --help)
Options:
    -i=<path_to_dumps>      Directory containing the metadata dumps
    -o=<path_to_output_dir>   Directory in which to put output files
"""
from docopt import docopt
import csv


def main(args):
    with open(args["-i"]) as f:
        reader = csv.reader(f, delimiter="\t")
        with open(args["-o"], "w") as g:
            writer = csv.writer(g)
            writer.writerows(reader)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)
