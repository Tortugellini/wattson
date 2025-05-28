import random
import pytest

from pathlib import Path
from wattson.models.power_supply import Battery


# Establishing global variables.
BAD_LOCATION = r"/random/directory/string"
GOOD_LOCATION = r"/sys/class/power_supply/"

BAD_NAME = "ABC1"
GOOD_NAME = "BAT0"

BAD_STRINGS_PROPERTIES = "random string"
BAD_LIST_PROPERTIES = ["x", random.random()]
GOOD_PROPERTIES = "serial_number, technology, manufacturer"


def get_battery(
    information_location: str,
    battery_name: str,
    properties: str | list
):
    """
    A convenience function for instantiating a 'Battery' object.
    ---
    Parameters:
        information_location, str: A directory.
        batter_name, str: A name.
        properties, str | list: A comma-separated-string or list of strings.
    """

    return Battery(
        information_location=information_location,
        battery_name=battery_name,
        properties=properties
    ) 

def test_check_location_with_bad_location():
    """
    Tests that the validation properly throws an error when provided
    a directory that doesn't exist.
    """

    with pytest.raises(FileNotFoundError):
        get_battery(BAD_LOCATION, GOOD_NAME, GOOD_PROPERTIES)

def test_check_location_with_good_location():
    """
    Tests that the validation properly throws an error when provided
    a directory that does exist.
    """
    
    battery = get_battery(GOOD_LOCATION, GOOD_NAME, GOOD_PROPERTIES)

    assert battery.information_location == Path(GOOD_LOCATION)

def test_check_battery_name_with_bad_name():
    """
    Tests that the validation properly throws an error when provided
    the name of a battery that does not exist.
    """

    with pytest.raises(FileNotFoundError):
        get_battery(BAD_LOCATION, BAD_NAME, GOOD_PROPERTIES)

def test_check_battery_name_with_good_name():
    """
    Tests that the validation properly throws an error when provided
    a battery name that does exist.
    """
    
    battery = get_battery(GOOD_LOCATION, GOOD_NAME, GOOD_PROPERTIES)

    assert battery.battery_name == GOOD_NAME

def test_check_properties_format_with_non_comma_separated_strings():
    """
    Tests that the validation properly throws an error when provided
    a bad 'properties' variable.
    """

    with pytest.raises(ValueError):
        get_battery(GOOD_LOCATION, GOOD_NAME, BAD_STRINGS_PROPERTIES)

def test_check_properties_format_with_list_of_not_strings():
    """
    Tests that the validation properly throws an error when provided
    a list containing non-strings.
    """

    with pytest.raises(ValueError):
        get_battery(GOOD_LOCATION, GOOD_NAME, BAD_LIST_PROPERTIES)

def test_check_properties_format_with_good_properties():
    """
    Tests that the validation properly throws an error when provided
    a good 'properties' variable.
    """

    battery = get_battery(GOOD_LOCATION, GOOD_NAME, GOOD_PROPERTIES)

    list_to_check_against = list(_ for _ in dir(battery) if not _.startswith("_"))
    list_to_check = list(map(lambda x: x in list_to_check_against, ["information_location", "battery_name", "properties"]))

    assert all(list_to_check)

def test_post_initialization():
    """
    Tests that the battery is initialized with
    information from the provided directory.
    """

    battery = get_battery(GOOD_LOCATION, GOOD_NAME, GOOD_PROPERTIES.split(", "))

    list_to_check_against = list(battery.model_extra.keys())
    list_to_check = list(map(lambda x: x in list_to_check_against, GOOD_PROPERTIES.split(", ")))

    assert all(list_to_check)
    