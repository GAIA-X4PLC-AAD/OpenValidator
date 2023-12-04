from checker_data import CheckerData


def check_positions(checker_data: CheckerData) -> None:
    # Check if Positions on road
    pass


def get_checker_id():
    return 'PositionChecker'


def get_description():
    return 'Checks positions in OSC file.'


def check(checker_data: CheckerData) ->None:
    check_positions(checker_data)