import logging
import os

base_url = None
api_key = None

__version__ = "1.1.0"
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger(name="OxAPI")
logger.setLevel(level=log_level)

try:
    api_key = os.environ["OXAPI_KEY"]
except KeyError:
    logger.warning(
        msg="API Key not found in environment variable 'OXAPI_KEY', you should set it manually"
    )

from requests import RequestException as _RequestException
from requests import get as _init_get

try:
    location = _init_get("https://ipinfo.io")
    if location.status_code == 200:
        location = location.json()
        if "country" not in location:
            logger.warning(msg="Unable to perform location check.")
        elif location["country"] != "US":
            logger.warning(
                msg="You are querying our API outside of the US. This results in significantly degraded performance."
            )
        else:
            logger.info("Querying from within the US. Enjoy the service!")
except _RequestException:
    logger.warning(msg="Unable to perform location check.")

from oxapi.asynch import AsyncCallPipe
from oxapi.config import default_api_version, default_model_version
from oxapi.nlp.classification import Classification
from oxapi.nlp.completion import Completion
from oxapi.nlp.encoding import Encoding
from oxapi.nlp.pipeline import Pipeline
from oxapi.nlp.transformation import Transformation

default_api_version: str = default_api_version
default_model_version: str = default_model_version
