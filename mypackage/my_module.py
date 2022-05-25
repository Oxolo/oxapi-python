# -*- coding: utf-8 -*-
"""Documentation for the module goes here.

The documentation must adhere to the Google format for docstrings. A
comprehensive example_ for such format could be useful.

.. _example:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""

import logging
from typing import Union

logger = logging.getLogger(__name__)


def sum_positive_numbers(
    number1: Union[int, float], number2: Union[int, float]
) -> float:
    """This is a sample function. It sums two positive integer or float numbers
    and returns a float number.

    Args:
      number1 (int or float): first positive number
      number2 (int or float): second positive number

    Returns:
      float : result of number1+number2
    """

    # Type check is mandatory for all input arguments for public interfaces
    # clear Error messages is required
    if not isinstance(number1, (int, float)):
        raise TypeError(f"number1 should be int or float while it is {type(number1)}")

    if not isinstance(number2, (int, float)):
        raise TypeError(f"number2 should be int or float while it is {type(number2)}")

    # optional Value checking. It is recommended since it will save time for
    # debugging in the future
    if not number1 > 0:
        raise ValueError(f"number1 should be greater than zero while it is {number1}")

    if not number2 > 0:
        raise ValueError(f"number2 should be greater than zero while it is {number2}")

    return float(number1 + number2)
