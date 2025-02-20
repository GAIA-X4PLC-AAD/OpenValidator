Envited OpenMSL QualityChecker bundle for ASAM OpenDRIVE
====

# Description
This repository contains, in addition to the ASAM QualityChecker CheckerBundles, simulation specific checks for the ASAM OpenDRIVE format. 

ASAM Quality Checker Framework: https://www.asam.net/standards/asam-quality-checker/

# Checks
The checks are located in the "checks" folder and the corresponding test example in the "examples" folder.

- geometry
  - road_geometry_length.py: Length of geometry elements shall be greater than epsilon and need to match with start of next elemen
  - road_geometry_parampoly3_attributes.py: ParamPoly3 parameters @aU, @aV and @bV shall be zero, @bU shall be > 0
  - road_min_length.py: Road Length shall be greater than epsilon
    
- linkage
  - crg_reference.py: heck reference to OpenCRG files

- semantic
  - junction_connection_lane_link_id.py: linked Lane shall exist in connected LaneSection
  - junction_connection_lane_linkage_order.py: Lane Links of Junction Connections should be ordered from left to right
  - junction_connection_road_linkage.py: Connection Roads need Predecessor and Successor. Connection Roads should be registered in Connection
  - junction_driving_lanes_continue.py: check road lane links of juction connection - each driving lane of the incoming roads must have a connection in the junction
  - road_lane_id_order.py: lane order should be continous and without gaps
  - road_lane_link_id.py: linked Lane shall exist in connected LaneSection
  - road_lane_property_sOffset.py: lane sOffsets (must be ascending, not too high) and sometimes be zero
  - road_lane_type_none.py: Lane Type shall not be None
  - road_lane_width.py: Lane width must always be greater than 0 or at the start/end point of a lanesection >= 0
  - road_lanesection_min_length.py: Length of lanesections shall be greater than epsilon
  - road_lanesection_s.py: Check starting sOffset of lanesections
  - road_link_backward.py: check if linked elements are also linked to original element
  - road_link_id.py: checks if linked Predecessor/Successor road/junction exist
  - road_object_position.py: check if object position is valid - s value is in range of road length, t and zOffset in range
  - road_object_size.py: check if object size is valid - width and length, radius and height in range
  - road_signal_object_lane_linkage.py: Linked Lanes should exist and orientation should match with driving direction
  - road_signal_position.py: check if signal position is valid - s value is in range of road length, t and zOffset in range
  - road_signal_size.py: check if signal size is valid - width and height in range
 
- statistic
  - statistic.py: Prints infos, about the content of OpenDRIVE file (signals, objects, road length)
 
# Usage
see ASAM qc-opendrive: https://github.com/asam-ev/qc-opendrive
