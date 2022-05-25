# -*- coding: utf-8 -*-
"""Documentation for the module goes here.

The documentation must adhere to the Google format for docstrings. A
comprehensive example_ for such format could be useful.

.. _example:
    http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""

# pylint: disable=wrong-import-position
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))
import logging
from pathlib import Path

import configargparse

from mypackage.my_module import sum_positive_numbers

# pylint: enable=wrong-import-position

logger = logging.getLogger(__name__)
logger.info("This is the module level logger")


def conf_parser():
    parser = configargparse.ArgumentParser(
        description="Start ... ",
        default_config_files=[str(Path(__file__).parent.parent / "config.ini")],
    )
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        is_config_file=True,
        env_var="config",
        help="config file path",
    )
    parser.add_argument(
        "--log_level",
        dest="log_level",
        action="store",
        env_var="log_level",
        default="INFO",
        type=str,
    )
    params_out = parser.parse_args()
    return params_out


def set_logger(params):
    if not logger.handlers:
        handler = logging.StreamHandler(stream=None)
        formatter = logging.Formatter(
            "%(asctime)15s : %(process)s.%(processName)s.%(module)s.%(funcName)s : "
            "%(levelname)s : %(message)s"
        )
        handler.setFormatter(formatter)

        if params.log_level == "INFO":
            handler.setLevel(logging.INFO)
        elif params.log_level == "DEBUG":
            handler.setLevel(logging.DEBUG)
        else:
            raise ValueError(
                f"LOG_LEVEL should be either INFO or DEBUG while it is {params.log_level}"
            )
        logger.addHandler(handler)


if __name__ == "__main__":

    # load the config.ini file
    params = conf_parser()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    set_logger(params)
    logger.info("sum of 2+2 is {%f}", sum_positive_numbers(2, 2))
