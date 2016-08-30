# Topic Contribs #
Module for analyzing contributions to a topic on Wikipedia.

## installation ##

    git clone https://github.com/WikiEducationFoundation/TopicContribs.git
    cd TopicContribs
    python3 setup.py install

## usage ##

    > python3 -m topics.cmdline
    cmdline
    Usage:
        cmdline --dumps=<path_to_dumps> --out=<path_to_output_dir>
                [--apm=<article_project_path>] [--pl=<project_list_path>]
                [--verbose] [<cohort_file> ... ]
        cmdline (-h | --help)
    Options:
        --dumps=<path_to_dumps>      Directory containing the metadata dumps
        --out=<path_to_output_dir>   Directory in which to put output files
        --apm=<article_project_path> Path to a csv of page_id project_name pairs.
        --pl=<project_list_path>     Path to a csv with all project_name's that you
                                        would like to be included in the count.
        <cohort_file>                File containing usernames of interest.
        -v, --verbose                Generate verbose output.

## Input files ##
### `path_to_dumps` ###
These must be full history dumps.
- For minimal size and maximal parallelization use
  `<wiki>-<date>-stub-meta-history<number>.xml.gz`
- If you want to use a single file
  `<wiki>-<date>-stub-meta-history.xml.gz`
- If you already have the full text history dumps downloaded and you feel like
  using them `<wiki>-<date>-pages-meta-history<number>.xml-<page_range>.bz2`
  will work.

### `article_project_path` ###
This file provides a map between articles are the projects they are included in.
We expect it to be a `.csv` following the format

    <page_id>,<project_name>

#### Generating this file ####
This file can be produced by running `sql/page_project_map.sql` on `wmflabs`
and replacing `<user_database>` with your user database.


### `project_list_path` ###
This is a file listing all of the project names we are interested in. The
names must match those in the `project_name` column of the
`article_project_path` file in order for the corresponding pages to be counted.

### `cohort_file` ###
A file or set of files listing the usernames of the users we are interested in
tracking. If multiple are used then each will be summed separately and output
to a separate output file.

## Output files ##
We will output one timeseries file for each `cohort_file` and one extra
`general` file for all activity.
