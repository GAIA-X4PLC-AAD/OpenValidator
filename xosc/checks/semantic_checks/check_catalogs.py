from checker_data import CheckerData


def check_conventions(checker_data: CheckerData) -> None:
    #Checks OpenSCENARIO conventions (according to standard)
    pass

def get_checker_id():
    return 'CatalogChecker'


def get_description():
    return 'Checks provided catalogs in OSC file.'


def check(checker_data: CheckerData) ->None:
    check_conventions(checker_data)