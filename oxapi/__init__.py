import logging
import os

base_url = None
api_version: str = "v1"
api_key = None
log_level = logging.INFO
logger = logging.getLogger(name="OxAPI Logger")
logger.setLevel(level=log_level)

try:
    api_key = os.environ["OXAPI_KEY"]
except KeyError:
    logger.warning(
        msg="API Key not found in evironment variable 'OXAPI_KEY', you should set it manually"
    )
