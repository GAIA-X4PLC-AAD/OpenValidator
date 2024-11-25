# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, Envited OpenMSL
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity

from openmsl_qc_opendrive import constants
from openmsl_qc_opendrive.base import models, utils

CHECKER_ID = "check_openmsl_xodr_junction_connection_lane_link_id_validity"
CHECKER_DESCRIPTION = (
    "linked Lane shall exist in connected LaneSection"
)
CHECKER_PRECONDITIONS = ""#basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "openmsl.net:xodr:1.7.0:road.semantic.junction_connection_lane_link_id_validity"

def _check_all_junctions(checker_data: models.CheckerData) -> None:
    roads = utils.get_road_id_map(checker_data.input_file_xml_root)
    junctions = utils.get_junctions(checker_data.input_file_xml_root)

    for junction in junctions:
        junctionID = junction.attrib["id"]
        connections = utils.get_connections_from_junction(junction)

        for connection in connections:
            connectionID = connection.attrib["id"]
            connectedLaneSections = utils.get_incoming_and_connection_contacting_lane_sections(connection, roads)

            laneLinks = utils.get_lane_links_from_connection(connection)
            for laneLink in laneLinks:
                issue_descriptions = []
                laneFrom = utils.get_from_attribute_from_lane_link(laneLink)
                laneTo = utils.get_to_attribute_from_lane_link(laneLink)

                connectedLane = utils.get_lane_from_lane_section(connectedLaneSections.incoming, laneFrom)
                if laneFrom == 0:
                    issue_descriptions.append(f"junction {junctionID} Connection {connectionID} has invalid lane linkage : 0")
                elif connectedLane is None:
                    issue_descriptions.append(f"junction {junctionID} Connection {connectionID} has invalid lane linkage : laneFrom not found")

                connectedLane = utils.get_lane_from_lane_section(connectedLaneSections.connection, laneTo)
                if laneTo == 0: 
                    issue_descriptions.append(f"junction {junctionID} Connection {connectionID} has invalid lane linkage : 0")
                elif connectedLane is None:
                    issue_descriptions.append(f"junction {junctionID} Connection {connectionID} has invalid lane linkage : laneTo not found")

                for description in issue_descriptions:
                    # register issues
                    issue_id = checker_data.result.register_issue(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        description=description,
                        level=IssueSeverity.WARNING,
                        rule_uid=RULE_UID,
                    )
                    # add xml location
                    checker_data.result.add_xml_location(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        issue_id=issue_id,
                        xpath=checker_data.input_file_xml_root.getpath(laneLink),
                        description=description,
                    )


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: openmsl.net:xodr:1.7.0:road.semantic.junction_connection_lane_link_id_validity

    Description: linked Lane shall exist in connected LaneSection.

    Severity: WARNING

    Version range: [1.7.0, )

    Remark:
        TODO
    """
    logging.info("Executing road.semantic.junction_connection_lane_link_id_validity check.")

    _check_all_junctions(checker_data)
