from result_report import IssueLevel, FileLocation
from checker_data import CheckerData
from pathlib import Path
from sys import platform

import urllib.request
import subprocess
import logging
import zipfile
import shutil
import os

def get_filepath() -> Path:    
    esmini_exec = Path('esmini') / 'esmini' / 'bin'
    if platform == 'linux' or platform == 'linux2': # linux
        esmini_exec = esmini_exec / 'esmini'
    elif platform == 'darwin': # OS X    
        esmini_exec = esmini_exec / 'esmini'
    elif platform == 'win32': # Windows  
        esmini_exec = esmini_exec / 'esmini.exe'      
    else:
        logging.error(f'Unknown OS used. Cannot determine esmini installation.')
        raise Exception('Could not determine operating system.')        
    return esmini_exec


def get_URL() -> str: 
    url = 'https://github.com/esmini/esmini/releases/latest/download/'
    if platform == 'linux' or platform == 'linux2': # linux
        url = url + 'esmini-bin_Linux.zip'
    elif platform == 'darwin': # OS X    
        url = url + 'esmini-bin_macOS.zip'
    elif platform == 'win32': # Windows  
        url = url + 'esmini-bin_Windows.zip'  
    else:
        logging.error(f'Unknown OS used. Cannot determine esmini installation.')
        raise Exception('Could not determine operating system.')        
    return url


def find_esmini():
    esmini_exec = shutil.which('esmini')
    # check if installed
    if esmini_exec is not None: 
        logging.debug(f'Found system esmini installation: {esmini_exec}')
        esmini_exec = Path(esmini_exec)
    else:
        # check if exist local
        esmini_exec_local =  get_filepath()
        print(esmini_exec_local.absolute())
        if esmini_exec_local.exists():
            esmini_exec = esmini_exec_local
            logging.debug(f'Using local esmini installation: {esmini_exec}')
        else:
            # download
            out_file = Path('esmini.zip')
            esmini_exec = esmini_exec_local
            print(out_file.absolute())
            if not out_file.exists():
                logging.debug('No esmini installation found. Downloading it...')
                url = get_URL()            
                logging.debug(f'Retrieving from {url}')
                urllib.request.urlretrieve(url, out_file)

            # extract zip
            logging.debug(f'Extracting esmini')
            extract_path = Path('esmini')
            if extract_path.exists():
                shutil.rmtree(extract_path) # remove first if folder exist
            with zipfile.ZipFile(out_file, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # change exucution rights
            os.chmod(str(esmini_exec), 0o555)
            os.remove(out_file)

    print(esmini_exec)            
    return esmini_exec


def get_checker_id():
    return 'SimulatorESMINICheck'


def get_description():
    return 'Checks compatibility with ESMINI simulator.'


def check(checker_data: CheckerData):
    esmini_exec = find_esmini()
    if esmini_exec is None:
        logging.warning(f'Could not find any esmini executable in PATH')
        checker_data.checker.gen_issue(IssueLevel.WARNING,
                            'Could not check esmini compatibility. No esmini executable in PATH.',
                            [FileLocation(checker_data.file)])
        return
    logging.debug(f'Using esmini installation {esmini_exec}')

    res = subprocess.run([str(esmini_exec.absolute()), 
                    '--window', '0', '0', '0', '0',
                    '--headless',
                    '--fixed_timestep', '0.05',
                    '--disable_log',
                    '--osc', checker_data.file.resolve().absolute()],
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE)
    
    esmini_version = subprocess.run([str(esmini_exec.absolute()), 
                    '--version'],
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE).stdout.decode()
    checker_data.reporter.report_meta['simulation_check_esmini_tool_version'] = esmini_version

    logging.debug(f'Esmini output:\n{res.stdout.decode()}')
    if res.returncode != 0:
        checker_data.checker.gen_issue(IssueLevel.WARNING,
                            f'Esmini compatibility failed. Process exited with non 0 exit status ({res.returncode})',
                            [FileLocation(checker_data.file)])
