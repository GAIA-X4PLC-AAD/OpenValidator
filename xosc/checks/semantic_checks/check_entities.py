from checker_data import CheckerData


def check_entities(checker_data: CheckerData) -> None:
    # entity bounding boxes shall not intersect
    pass


def get_checker_id():
    return 'EntitiyChecker'


def get_description():
    return 'Checks osc entities.'


def check(checker_data: CheckerData) ->None:
    check_entities(checker_data)