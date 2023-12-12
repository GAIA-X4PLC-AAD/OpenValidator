from result_report import IssueLevel
from checker_data import CheckerData

import logging

def report_num_nodes(checker_data: CheckerData, node_name: str):
    checker_data.checker.gen_issue(IssueLevel.INFORMATION, f'Number of {node_name}: {len(checker_data.data.findall(f".//{node_name}"))}')

def calc_frequency(checker_data: CheckerData) -> None:
    logging.info(get_checker_id())

    report_num_nodes(checker_data, 'road')
    report_num_nodes(checker_data, 'junction')

    # network length
    roads = checker_data.data.findall(f".//road")
    roadLengths = 0.0
    for road in roads:
        roadLengths += float(road.attrib["length"])
    checker_data.checker.gen_issue(IssueLevel.INFORMATION, f'RoadNetwork length {roadLengths} m')  

    report_num_nodes(checker_data, 'signal')
    report_num_nodes(checker_data, 'object')
    
    #signals
    signals = checker_data.data.findall(f".//signal")
    signal_types = dict()
    for signal in signals:
        type_str = f'{signal.attrib['type']}_{signal.attrib['subtype']}'
        if type_str in signal_types:
            signal_types[type_str] = signal_types[type_str] + 1
        else:
            signal_types[type_str] = 1
    
    sorted_signal_type = sorted(signal_types.items())
    for key, count in sorted_signal_type:
        checker_data.checker.gen_issue(IssueLevel.INFORMATION, f'Numer of Signal type {key}: {count}')    

    # objects
    objects = checker_data.data.findall(f".//object")
    object_types = dict()
    for object in objects:
        type_str = f'{object.attrib['type']}'
        if type_str in object_types:
            object_types[type_str] = object_types[type_str] + 1
        else:
            object_types[type_str] = 1
    
    sorted_object_type = sorted(object_types.items())            
    for key, count in sorted_object_type:
        checker_data.checker.gen_issue(IssueLevel.INFORMATION, f'Numer of object type {key}: {count}')   

def get_checker_id():
    return 'calculate frequency'


def get_description():
    return 'calculates the frequency of node elements (road, junction) and object and signal types.'


def check(checker_data: CheckerData) ->None:
    calc_frequency(checker_data)