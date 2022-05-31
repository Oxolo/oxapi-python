import configparser
import logging
import os

from oxapi.asynch import AsyncCallPipe
from oxapi.nlp.classification import Classification
from oxapi.nlp.completion import Completion
from oxapi.nlp.encoding import Encoding
from oxapi.nlp.pipeline import Pipeline
from oxapi.nlp.transformation import Transformation

from oxapi.config import version, log_level, default_api_version, default_model_version

base_url = None
api_key = None
"""config = configparser.ConfigParser()

try:
    with open("config.ini") as f:
        config_file_path = "config.ini"
        # Do something with the file
except IOError:
    config_file_path = "../config.ini"

print(config_file_path)
config.read(config_file_path)"""

__version__: str = version #config["DEFAULT"]["version"]
log_level = log_level #config["DEFAULT"]["log_level"]
logger = logging.getLogger(name="OxAPI Logger")
logger.setLevel(level=log_level)

default_api_version: str = default_api_version #config["DEFAULT"]["default_api_version"]
default_model_version: str = default_model_version #config["DEFAULT"]["default_model_version"]


try:
    api_key = os.environ["OXAPI_KEY"]
except KeyError:
    logger.warning(
        msg="API Key not found in environment variable 'OXAPI_KEY', you should set it manually"
    )
