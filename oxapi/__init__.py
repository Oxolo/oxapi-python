import logging
import os

from oxapi.asynch import AsyncCallPipe
from oxapi.config import default_api_version, default_model_version, log_level, version
from oxapi.nlp.classification import Classification
from oxapi.nlp.completion import Completion
from oxapi.nlp.encoding import Encoding
from oxapi.nlp.pipeline import Pipeline
from oxapi.nlp.transformation import Transformation

base_url = None
api_key = None

__version__: str = version
log_level = log_level
logger = logging.getLogger(name="OxAPI Logger")
logger.setLevel(level=log_level)

default_api_version: str = default_api_version
default_model_version: str = default_model_version


try:
    api_key = os.environ["OXAPI_KEY"]
except KeyError:
    logger.warning(
        msg="API Key not found in environment variable 'OXAPI_KEY', you should set it manually"
    )
