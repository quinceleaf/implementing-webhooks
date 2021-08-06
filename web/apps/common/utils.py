def check_if_all_bool(*, elements: list) -> bool:
    """Check if all elements in list are either True or False"""

    result = True
    for element in elements:
        if not isinstance(element, bool):
            return False

    return result


def check_if_all_none(*, elements: list) -> bool:
    """Check if all elements in list are None"""

    result = True
    for element in elements:
        if element is not None:
            return False

    return result


def check_if_mixed_bool_and_none(*, elements: list) -> bool:
    """Check if elements in list are mix of boolean values (True/False) and None (neither all one or the other)"""

    found_bool = False
    found_none = False
    for element in elements:
        if isinstance(element, bool):
            found_bool = True
        if element is None:
            found_none = True

    if all([found_bool, found_none]):
        return True
    else:
        return False
