# Checker Lib
the Checker Lib checks files/folders for validity. The framework has a flexible structure so that further formats, categories, checks and output formats can be added.
The following are currently checked
- ASAM OpenDRIVE 1.1 - 1.7
- ASAM OpenSCENARIO 0.9.1 - 1.1.0

# Motivation
We want to achieve a free, comprehensive and uniform validation of ASAM OpenX Standards

# Installation / How to setup

1. **Clone this git repository:** ``` git clone https://github.com/GAIA-X4PLC-AAD/OpenValidator ```

2. **Install python** (https://www.python.org/, used python version: Python 3.12.0)

    How to check current version on windows: ```py --version```
    How to check current version on macOS: ```python3 --version```

3. **Install packages with pip**

    How to check current version on windows: ```py -m pip --version```
    How to check current version on macOS: ```python3 -m pip --version```

    **Needed packages:**

| name            | used version | installation link for windows     | installation link for macOS            |
|-----------------|--------------|-----------------------------------|----------------------------------------|
| lxml            | 4.9.3        | py -m pip install lxml            | python3 -m pip install lxml            |
| scipy           | 1.21.6       | py -m pip install scipy           | python3 -m pip install scipy           |

# Development
Used integrated development environment: Visual Studio Code version 1.84.2

# How to run
1. Open your console/terminal
2. Navigate to cloned folder from GitHub with the main.py in it
3. Use on windows: ```py main.py``` or on macOS: ```python3 main.py```
4. Use following arguments:
    - ```  file(s) or folder to validate```
    - ```-f  Specification of the formats to be checked (file extension or check folder), e.g. xodr for OpenDrive.```
    - ```-a  Additional directories for validation checks.```
    - ```-c  Path to config file. Otherwise the config is taken from the format folder```
    - ```-o  Path to validation report folder```
    - ```-t  Output format of result report (available: xqar, json, txt)```
    - ```-e  Should the script be terminated after an error ('exit-if-error') or not ('no-exit').```

5. You will find the result file in validation report folder.

# How to build and run with Docker
1. Open your console/terminal
2. Navigate to cloned folder from GitHub with the Dockerfile in it
3. Build the docker image with: ```docker build . -t open_validator```
4. Run the docker image with: ```docker run -it --rm -v PATH_TO_DATA_FOLDER:/app/data/  open_validator i data/inputs/sampleODR -o data/outputs -e true```
5. notes:
    - PATH_TO_DATA_FOLDER is the path to the folder where the input data is stored in it and output data will be stored in it, e.g. "/home/user/data" or "C:\Users\user\data" or simply "data" (when you are in the folder where the data folder is in it).
    - data folder must contains a folder named "inputs". This folder must contains the file you want to parse, e.g sampleODR.
    - "-i data/inputs/sampleODR" is the path to the file you want to parse.
    - "-o data/outputs" is the path to the folder where the parsed file should be stored.
    - "-e true" is the argument to exit the script if an error occurs.
6. You will find the parsed file in the "PATH_TO_DATA_FOLDER/outputs".

# How to build and run with docker-compose
If you do not want to build the docker image yourself, and you have already installed docker on your machine, you can use following steps to run the docker image with docker-compose:
1. Open your console/terminal
2. Navigate to cloned folder from GitHub with the docker-compose.yml in it
3. change the content of the data/inputs/sampleODR file with your own OpenDrive file
4. Run the docker image with: ```docker compose up```
5. You will find the parsed file in the "data/outputs".

# Structure
- Main.py
  - reads, checks parameters and for each file calls validation and writes output
- validator.py
  - loads registered bundles, loads and executes check
- result_report.py
  - Data structure for report file and functions for registering
  - Writes Report Tree as different formats
- [format]
   - folder for specific format
   - config.json
     - configuration for specific format
   - format.json
     - informatoin about format
   - [checks]
     - __init__.py
       - define category / bundle order
     - [categories]
       - __init__.py
         - category / bundle information, define check order
       - check_[type].py
         - individual check
   - [examples]
    - examples for each check and category

# Categories
- base checks
  - check if file exist and loadable
- schema checks
  - Test against schema file and check value type
- semantic checks
  - check links, order, ranges of main elements
- geometry checks
  - Checks the correctness of values, ranges and steadiness
- linkage
  - check to other files and check if references / position is correct
- tool compability
  - loadable / usable in applications
  - check special requirements of applications
- statistic
  - count elements and lengths

# Extension
To create a new check in an existing category, simply create a check_[type].py in the category folder and overwrite the following functions:
- get_checker_id
  - name of check
- get_description
  - description of check
- check(checker_data: CheckerData) ->bool:
  - actual check function
  - Return False if validation has to be cancelled

To create a new category, add a new folder under Checks and create an __init__.py with the following information:
- CHECKER_BUNDLE_NAME=[name]
- CHECKER_BUNDLE_DESCRIPTION=[Description]
- CHECKER_BUNDLE_VERSION=[Version]
- ORDER=[list of ordered checks] - optional

To add a new format create a format folder in the root (preferably the name of the FileExtension) and create and fill the
config.json and format.json

# Output
The result class currently outputs 3 formats
- txt simple text file with the issues per check
- json output as a json file
- xqar output as XML result file for QChecker

# Overview Checks
- List of tests defined in the context of GaiaX:
- https://ascs2008.sharepoint.com/:x:/r/sites/team/_layouts/15/Doc.aspx?sourcedoc=%7B32A490CB-E63E-4293-8063-DFB3136E0B6C%7D&file=Data_Validation.xlsx&action=default&mobileredirect=true