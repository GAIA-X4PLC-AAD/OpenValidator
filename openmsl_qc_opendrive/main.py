# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, Envited OpenMSL
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import argparse
import logging
import types
import sys
#import os

import sys
print(sys.path)

from qc_baselib import Configuration, Result, StatusType
from qc_baselib.models.common import ParamType

from openmsl_qc_opendrive import constants
from openmsl_qc_opendrive.checks import geometry
from openmsl_qc_opendrive.checks import linkage
from openmsl_qc_opendrive.checks import semantic
from openmsl_qc_opendrive.checks import statistic
from openmsl_qc_opendrive.checks import tool_compatibility_checks
from openmsl_qc_opendrive.base import models, utils

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def args_entrypoint() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="OpenMSL QC OpenDrive Checker",
        description="This is a collection of scripts for checking the validity for simulation tools of OpenDrive (.xodr) files.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--config_path")
    parser.add_argument("-g", "--generate_markdown", action="store_true")

    return parser.parse_args()


def execute_checker(
    checker: types.ModuleType,
    checker_data: models.CheckerData,
    required_definition_setting: bool = False,
) -> None:
    # Register checker
    checker_data.result.register_checker(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        description=checker.CHECKER_DESCRIPTION,
    )

    # Register rule uid
    checker_data.result.register_rule_by_uid(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=checker.CHECKER_ID,
        rule_uid=checker.RULE_UID,
    )

    # Check preconditions. If not satisfied then set status as SKIPPED and return
    if not checker_data.result.all_checkers_completed_without_issue(
        checker.CHECKER_PRECONDITIONS
    ):
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.SKIPPED,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME,
            checker.CHECKER_ID,
            "Preconditions are not satisfied. Skip the check.",
        )

        return

    # Checker definition setting. If not satisfied then set status as SKIPPED and return
    if required_definition_setting:
        schema_version = checker_data.schema_version

        splitted_rule_uid = checker.RULE_UID.split(":")
        if len(splitted_rule_uid) != 4:
            raise RuntimeError(f"Invalid rule uid: {checker.RULE_UID}")

        definition_setting = splitted_rule_uid[2]
        if (
            schema_version is None
            or utils.compare_versions(schema_version, definition_setting) < 0
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.SKIPPED,
            )

            checker_data.result.add_checker_summary(
                constants.BUNDLE_NAME,
                checker.CHECKER_ID,
                f"Version {schema_version} is lower than definition setting {definition_setting}. Skip the check.",
            )

            return

    # Execute checker
    try:
        checker.check_rule(checker_data)

        # If checker is not explicitly set as SKIPPED, then set it as COMPLETED
        if (
            checker_data.result.get_checker_status(checker.CHECKER_ID)
            != StatusType.SKIPPED
        ):
            checker_data.result.set_checker_status(
                checker_bundle_name=constants.BUNDLE_NAME,
                checker_id=checker.CHECKER_ID,
                status=StatusType.COMPLETED,
            )
    except Exception as e:
        # If any exception occurs during the check, set the status as ERROR
        checker_data.result.set_checker_status(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=checker.CHECKER_ID,
            status=StatusType.ERROR,
        )

        checker_data.result.add_checker_summary(
            constants.BUNDLE_NAME, checker.CHECKER_ID, f"Error: {str(e)}."
        )

        logging.exception(f"An error occur in {checker.CHECKER_ID}.")


def run_checks(config: Configuration, result: Result) -> None:
    checker_data = models.CheckerData(
        xml_file_path=config.get_config_param("InputFile"),
        input_file_xml_root=None,
        config=config,
        result=result,
        schema_version=None,
    )

    # Get xml root if the input file is a valid xml doc
    checker_data.input_file_xml_root = utils.get_root_without_default_namespace(checker_data.xml_file_path)

    # 1. Run semantic checks
    execute_checker(semantic.junction_connection_lane_link_id, checker_data)
    execute_checker(semantic.junction_connection_lane_linkage_order, checker_data)
    execute_checker(semantic.road_lane_link_id, checker_data)
    execute_checker(semantic.road_lane_type_none, checker_data)

    # 2. Run geometry checks
    execute_checker(geometry.road_geometry_length, checker_data)
    execute_checker(geometry.road_geometry_parampoly3_attributes, checker_data)
    execute_checker(geometry.road_min_length, checker_data)

    # 3. Run linkage checks
    execute_checker(linkage.crg_reference, checker_data)

    # 4. Run tool compatibility checks
    execute_checker(tool_compatibility_checks.road_type_vs_speed_limit, checker_data)

    # 5. Run tool statistic checks
    execute_checker(statistic.statistic, checker_data)


def main():
    args = args_entrypoint()

    logging.info("Initializing checks")

    config = Configuration()
    config.load_from_file(xml_file_path=args.config_path)

    result = Result()
    result.register_checker_bundle(
        name=constants.BUNDLE_NAME,
        description="OpenMSL OpenDrive checker bundle",
        version=constants.BUNDLE_VERSION,
        summary="",
    )
    result.set_result_version(version=constants.BUNDLE_VERSION)

    run_checks(config, result)

    result.copy_param_from_config(config)

    result.write_to_file(
        config.get_checker_bundle_param(
            checker_bundle_name=constants.BUNDLE_NAME, param_name="resultFile"
        ),
        generate_summary=True,
    )

    if args.generate_markdown:
        result.write_markdown_doc("generated_checker_bundle_doc.md")

    logging.info("Done")


if __name__ == "__main__":
    main()
