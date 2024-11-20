# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys

from typing import List

import openmsl_cb_opendrive.main as main

from openmsl_cb_opendrive import constants
from qc_baselib import Configuration, Result, IssueSeverity, StatusType

CONFIG_FILE_PATH = "bundle_config.xml"
REPORT_FILE_PATH = "xodr_bundle_report.xqar"


def create_test_config(target_file_path: str):
    test_config = Configuration()
    test_config.set_config_param(name="InputFile", value=target_file_path)
    test_config.register_checker_bundle(checker_bundle_name=constants.BUNDLE_NAME)
    test_config.set_checker_bundle_param(
        checker_bundle_name=constants.BUNDLE_NAME,
        name="resultFile",
        value=REPORT_FILE_PATH,
    )

    test_config.write_to_file(CONFIG_FILE_PATH)


def check_issues(
    rule_uid: str,
    issue_count: int,
    issue_xpath: List[str],
    severity: IssueSeverity,
    checker_id: str,
):
    result = Result()
    result.load_from_file(REPORT_FILE_PATH)

    assert result.get_checker_status(checker_id) == StatusType.COMPLETED

    issues = result.get_issues_by_rule_uid(rule_uid)

    assert len(issues) == issue_count

    locations = set()
    for issue in issues:
        for issue_location in issue.locations:
            for xml_location in issue_location.xml_location:
                locations.add(xml_location.xpath)

    for xpath in issue_xpath:
        assert xpath in locations

    for issue in issues:
        assert issue.level == severity


def check_skipped(
    rule_uid: str,
    checker_id: str,
):
    result = Result()
    result.load_from_file(REPORT_FILE_PATH)

    assert result.get_checker_status(checker_id) == StatusType.SKIPPED

    issues = result.get_issues_by_rule_uid(rule_uid)

    assert len(issues) == 0


def launch_main(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "-c", CONFIG_FILE_PATH, "--generate_markdown"],
    )
    main.main()


def cleanup_files():
    os.remove(REPORT_FILE_PATH)
    os.remove(CONFIG_FILE_PATH)
