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
4. Select the openDrive file you want to parse in the file dialog.
5. You will find the parsed file in the same file path as the source file.

# How to build and run with Docker
1. Open your console/terminal
2. Navigate to cloned folder from GitHub with the Dockerfile in it
3. Build the docker image with: ```docker build . -t open_validator```
4. Run the docker image with: ```docker run -it --rm -v PATH_TO_DATA_FOLDER:/app/data/  open_validator "/bin/bash" "/app/entrypoint.sh" "data/inputs/sampleODR" "data/outputs"```
5. notes:
    - PATH_TO_DATA_FOLDER is the path to the folder where the input data is stored in it and output data will be stored in it, e.g. "/home/user/data" or "C:\Users\user\data" or simply "data" (when you are in the folder where the data folder is in it).
    - data folder must contains a folder named "inputs". This folder must contains the file you want to parse, e.g sampleODR.
    - "data/inputs/sampleODR" is the path to the file you want to parse
    - "data/outputs" is the path to the folder where the parsed file should be stored
6. You will find the parsed file in the "PATH_TO_DATA_FOLDER/outputs".

# List of tests defined in the context of GaiaX:
 see
 https://ascs2008.sharepoint.com/:x:/r/sites/team/_layouts/15/Doc.aspx?sourcedoc=%7B32A490CB-E63E-4293-8063-DFB3136E0B6C%7D&file=Data_Validation.xlsx&action=default&mobileredirect=true