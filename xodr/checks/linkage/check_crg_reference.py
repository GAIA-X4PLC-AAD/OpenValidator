from result_report import IssueLevel, FileLocation, create_location_from_element
from checker_data import CheckerData
from pathlib import Path

import logging
import os

def check_crg_reference(checker_data: CheckerData) -> None:
    logging.info(get_checker_id())

    crgs = checker_data.data.findall(f".//CRG")
    for crg in crgs:
        crg_file = Path(crg.attrib['file'])
        abs_path = os.path.dirname(checker_data.file)
        abs_file = Path(os.path.abspath(os.path.join(abs_path, crg_file)))
        if not abs_file.exists():
            checker_data.checker.gen_issue(IssueLevel.WARNING, f'CRG file {abs_file} not exist.', [create_location_from_element(crg)])
    

def get_checker_id():
    return 'check crg reference'


def get_description():
    return 'check reference to OpenCRG files.'


def check(checker_data: CheckerData) ->None:
    check_crg_reference(checker_data)