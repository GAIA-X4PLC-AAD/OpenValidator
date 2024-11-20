# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, Envited OpenMSL
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from qc_baselib import IssueSeverity

from openmsl_qc_opendrive import constants
from openmsl_qc_opendrive.base import models, utils
from openmsl_qc_opendrive import basic_preconditions

CHECKER_ID = "check_openmsl_xodr_road_geometry_parampoly3_attributes_valid"
CHECKER_DESCRIPTION = (
    "ParamPoly3 parameters @aU, @aV and @bV shall be zero, @bU shall be > 0"
)
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "openmsl.net:xodr:1.7.0:road.geometry.parampoly3.attributes_valid"

TOLERANCE_THRESHOLD_BV = 0.001

def _check_all_roads(checker_data: models.CheckerData) -> None:
    roads = utils.get_roads(checker_data.input_file_xml_root)

    for road in roads:
        roadID = road.attrib["id"]

        geometry_list = utils.get_road_plan_view_geometry_list(road)
        for geometry in geometry_list:
            length = utils.get_length_from_geometry(geometry)
            if length is None:
                continue

            param_poly3 = utils.get_arclen_param_poly3_from_geometry(geometry)
            if param_poly3 is None:
                continue

            u = utils.poly3_to_polynomial(param_poly3.u)
            v = utils.poly3_to_polynomial(param_poly3.v)

            s_coordinate = utils.get_s_from_geometry(geometry)

            issue_descriptions = list
            if u.a != 0.0:                
                issue_descriptions.extend(f"road {roadID} has invalid paramPoly3 : aU != 0.0 ({u.a}) at s={s_coordinate}")

            if v.a != 0.0:
                issue_descriptions.extend(f"road {roadID} has invalid paramPoly3 : aV != 0.0 ({u.a}) at s={s_coordinate}")

            if abs(v.b) > TOLERANCE_THRESHOLD_BV:
                issue_descriptions.extend(f"road {roadID} has invalid paramPoly3 : abs(bV) > {TOLERANCE_THRESHOLD_BV} ({v.b}) at s={s_coordinate}")              

            if u.b <= 0.0:
                issue_descriptions.extend(f"road {roadID} has invalid paramPoly3 : bU <= 0.0 ({u.b}) at s={s_coordinate}")

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
                    xpath=checker_data.input_file_xml_root.getpath(geometry),
                    description=description,
                )

                if s_coordinate is None:
                    continue

                s_coordinate += length / 2.0

                # add 3d point
                inertial_point = utils.get_point_xyz_from_road_reference_line(road, s_coordinate)
                if inertial_point is not None:
                    checker_data.result.add_inertial_location(
                        checker_bundle_name=constants.BUNDLE_NAME,
                        checker_id=CHECKER_ID,
                        issue_id=issue_id,
                        x=inertial_point.x,
                        y=inertial_point.y,
                        z=inertial_point.z,
                        description=description,
                    )


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: openmsl.net:xodr:1.7.0:road.geometry.parampoly3.attributes_valid

    Description: ParamPoly3 parameters @aU, @aV and @bV shall be zero, @bU shall be > 0.

    Severity: WARNING

    Version range: [1.7.0, )

    Remark:
        TODO
    """
    logging.info("Executing road.geometry.parampoly3.attributes_valid check.")

    _check_all_roads(checker_data)
