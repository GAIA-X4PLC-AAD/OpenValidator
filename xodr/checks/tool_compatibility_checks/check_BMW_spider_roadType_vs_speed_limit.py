from xodr.checks.semantic_checks.semantic_utilities import LaneSection
from result_report import IssueLevel, create_location_for_road
from checker_data import CheckerData 
from lxml import etree

import logging


def get_speed_value(speed: etree._Element) -> float:
    speedUnit = 'm/s'
    if 'unit' in speed.attrib:
        speedUnit = speed.attrib['unit']
    speedvalue = float(speed.attrib['max'])
    if speedUnit == 'm/s':
        speedvalue = speedvalue * 3.6
    elif speedUnit == 'mph':
        speedvalue = speedvalue * 1.609
    elif speedUnit == 'km/h':
        speedvalue = speedvalue
    return speedvalue


def check_lane_speed(laneSection: LaneSection, speed_ranges: str, side: str, checker_data: CheckerData) -> None:
    laneSide = laneSection.treeElement.find(side)
    if laneSide == None:
        return                          # no lanes on this side
    
    for lane in laneSide.findall("./lane"):
        laneType = lane.attrib['type']
        if laneType != 'driving':                                           # TODO mehr Lanetypen
            continue                        # only check driving lanes

        laneID = lane.attrib["id"]
        for speed in lane.findall("./speed"):
            speedvalue = get_speed_value(speed)            
            if speed_ranges['min'] > speedvalue or speed_ranges['max'] < speedvalue:
                message = f"road {laneSection.roadId} laneSection {laneSection.startS} lane {laneID} has speed value {speedvalue}km/h that is outside the valid range ({speed_ranges['min']} - {speed_ranges['max']})"
                checker_data.checker.gen_issue(IssueLevel.INFORMATION, message, create_location_for_road(speed, laneSection.roadId, laneSection.startS, None))
            

# check road length with sum of geometry parts
def check_BMW_spider_roadType_vs_speed_limit(checker_data: CheckerData) -> None:  
    logging.info(get_checker_id())
    
    for road in checker_data.data.findall("./road"):
        if road.find("type") is None:
            continue                        # nothing to check, if no roadtype is given

        roadID = road.attrib["id"]
        roadType = road.find("type").attrib["type"]
        speed_ranges = checker_data.config['speed_ranges']
        if not roadType in speed_ranges:
            message = f"road {roadID} has invalid road type {roadType} or it is missing in config file"
            checker_data.checker.gen_issue(IssueLevel.WARNING, message, create_location_for_road(road, roadID, None, None))
            continue

        for laneSectionElement in road.findall("./lanes/laneSection"):
            laneSection = LaneSection(road, laneSectionElement)
            check_lane_speed(laneSection, speed_ranges[roadType], "left", checker_data)
            check_lane_speed(laneSection, speed_ranges[roadType], "right", checker_data)


def get_checker_id():
    return 'check BMW Spider RoadType vs SpeedLimit'


def get_description():
    return 'check if road type have valid speed limit'


def check(checker_data: CheckerData):
    check_BMW_spider_roadType_vs_speed_limit(checker_data)