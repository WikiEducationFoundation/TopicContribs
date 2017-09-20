"""cmdline
Usage:
    cmdline --dumps=<path_to_dumps> --out=<path_to_output_dir>
            [--apm=<article_project_path>] [--pl=<project_list_path>]
            [--threads=<num_threads>]
            [--verbose] [<cohort_file> ... ]
    cmdline (-h | --help)
Options:
    --dumps=<path_to_dumps>      Directory containing the metadata dumps
    --out=<path_to_output_dir>   Directory in which to put output files
    --apm=<article_project_path> Path to a csv of page_id project_name pairs.
    --pl=<project_list_path>     Path to a csv with all project_name's that you
                                    would like to be included in the count.
    --threads=<num_threads>      Number of threads to be used. All available
                                    will be used if not specified.
    <cohort_file>                File containing usernames of interest.
    -v, --verbose                Generate verbose output.
"""
from docopt import docopt
import re
import os
import logging
from os import listdir
from os.path import isfile, join
from . import extract
import csv


def _get_files_to_work_on(input_dir):
    raw_files = [join(input_dir, f) for f in listdir(input_dir)
                 if isfile(join(input_dir, f))]
    dump_files = [f for f in raw_files
                  if re.match('.*stub-meta-history(\d+).xml', f)]
    return dump_files


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def output_results(results, output_dir):
    for cohort, result in results.items():
        filename = "{0}.csv".format(cohort)
        with open(join(output_dir, filename), "w") as f:
            writer = csv.writer(f)
            sorted_results = sorted(result.items(), key=lambda x: x[0])
            for key, value in sorted_results:
                writer.writerow([key, value])


def main(args):
    if args["--verbose"]:
        logging.basicConfig(level=logging.INFO)
    create_dir_if_not_exists(args["--out"])
    dump_paths = _get_files_to_work_on(args["--dumps"])
    cohorts = extract.load_cohorts(args["<cohort_file>"])
    pages = extract.get_pages_of_interest(args["--pl"],
                                          args["--apm"])
    results = extract.analyse_dumps(
        dump_paths, cohorts, pages, threads=int(args["--threads"])
    )
    output_results(results, args["--out"])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)
