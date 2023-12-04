# OpenDRIVE® validator
validate OpenDRIVE® files (.xodr) for schema, semantic, geometry in the context of GaiaX.  
Link to test tabel: https://ascs2008.sharepoint.com/:x:/r/sites/team/_layouts/15/Doc.aspx?sourcedoc=%7B32A490CB-E63E-4293-8063-DFB3136E0B6C%7D&file=Data_Validation.xlsx&action=default&mobileredirect=true

# Motivation
We want to achieve a free, comprehensive and uniform validation of OpenDRIVE® data

# Installation / How to setup

1. **Clone this git repository:** ``` git clone https://github.com/GAIA-X4PLC-AAD/map-and-scenario-data.git ```

2. **Install python** (https://www.python.org/, used python version: Python 3.11.2)

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


# List of tests defined in the context of GaiaX:
 see 
 https://ascs2008.sharepoint.com/:x:/r/sites/team/_layouts/15/Doc.aspx?sourcedoc=%7B32A490CB-E63E-4293-8063-DFB3136E0B6C%7D&file=Data_Validation.xlsx&action=default&mobileredirect=true