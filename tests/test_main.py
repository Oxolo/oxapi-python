# -*- coding: utf-8 -*-


import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))
import logging

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


# def test_set_logger():
#     """
#     stupid test to test an stupid function. No assert is here!
#     Returns:
#
#     """
#     params = mut.conf_parser()
#     assert params is not None
#     mut.set_logger(params)
