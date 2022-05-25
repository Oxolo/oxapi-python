# -*- coding: utf-8 -*-


import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))
import logging

import pytest

import mypackage.my_module as mut

logger = logging.getLogger()  # this will return the root logger.
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)15s : %(module)s.%(funcName)s :" " %(levelname)s : %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def test_sum_positive_numbers():
    # Benchmark testing
    result = mut.sum_positive_numbers(2, 3.0)
    assert result == 5.0
    assert isinstance(result, float)

    # Optional TypeError test
    with pytest.raises(TypeError):
        mut.sum_positive_numbers("s", 2)

    with pytest.raises(TypeError):
        mut.sum_positive_numbers(2, "s")

    # Optional ValueError testing
    with pytest.raises(ValueError):
        mut.sum_positive_numbers(-2, 2)

    # Optional ValueError testing
    with pytest.raises(ValueError):
        mut.sum_positive_numbers(2, -2)
