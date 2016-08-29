from functools import partial
import mwxml
import csv
import ntpath
from collections import Counter
import logging
from . import revhistory


def get_pages_of_interest(projects_filepath, project_page_map_filepath):
    with open(projects_filepath) as f:
        reader = csv.reader(f)
        projects = [r[0] for r in reader]
    with open(project_page_map_filepath) as f:
        reader = csv.reader(f)
        pages = [int(r[0]) for r in reader if r[2] in projects]
    return pages


def load_cohorts(cohort_files_paths):
    cohorts = {}
    for cfp in cohort_files_paths:
        c_name = ntpath.basename(cfp).split(".")[0]
        with open(cfp) as f:
            reader = csv.reader(f)
            cohorts[c_name] = [r[0] for r in reader]
    return cohorts


def analyse_dumps(dumps, cohorts, pages):
    results = _init_cohort_contribs(cohorts)
    _partial = partial(_analyse_single_dump, cohorts=cohorts, pages=pages)
    for sub_res in mwxml.map(_partial, dumps):
        for cohort in sub_res:
            results[cohort].update(sub_res[cohort])
    return results


def _analyse_single_dump(dump, path, cohorts, pages):
    logging.info("Working on {0}".format(path))
    cohort_contribs = _init_cohort_contribs(cohorts)
    for page in dump:
        if page.namespace != 0 or (pages is not None and page.id not in pages):
            continue
        history = revhistory.RevHistory(page)
        prev_bytes = 0
        for rev in history.revert_free_revisions():
            if (rev.deleted.text is True or
                    rev.deleted.comment is True or
                    rev.deleted.user is True or
                    rev.deleted.restricted is True):
                continue
            size = max(rev.bytes - prev_bytes, 0)
            date = rev.timestamp.strftime("%Y-%m-%d")
            for name in cohort_contribs:
                if (name == "general") or (rev.user.text in cohorts[name]):
                    cohort_contribs[name][date] += size
    logging.info("Finished {0}".format(path))
    yield cohort_contribs


def _init_cohort_contribs(cohorts):
    cc = {key: Counter() for key in cohorts}
    cc["general"] = Counter()
    return cc
