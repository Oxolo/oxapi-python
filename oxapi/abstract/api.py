from enum import Enum

import requests

import oxapi
from oxapi.error import (
    InvalidAPIKeyException,
    NotAllowedException,
    NotFoundException,
    OxAPIError,
)
from oxapi.utils import OxapiType


class ModelAPI:
    """General class for all the classes that call a OxAPI model.

    This class cannot be directly instantiated.
    """

    def __init__(
        self, model: Enum, oxapi_type: OxapiType, api_version: str, version: str
    ):
        """Constructor.

        Args:
            model: model to be invoked by the API.
            oxapi_type: type of OxAPI to call (NLP, CV etc.).
            api_version: version of the API.
            version: version of the model called by the API.
        """
        if self.__class__ == ModelAPI:
            raise NotImplementedError("ModelAPI class cannot be directly instantiated")
        self.model = model
        self.type: OxapiType = oxapi_type
        self.version = version
        self.api_version = api_version
        self.error = None
        self._body = None
        self.result = None

    def __repr__(self) -> str:
        return "Model: {0}, Type: {1}, API version: {2}, Version: {3}, Result: {4}, Error: {5}".format(
            self.model.value,
            self.type.value,
            self.api_version,
            self.version,
            str(self.result),
            str(self.error),
        )

    def __str__(self) -> str:
        return self.__repr__()

    def get_url(self, verbose: bool = False) -> str:
        """Function to build the full API url.

        Args:
            verbose (bool): optional, True to enable verbose mode.

        Returns:
            str : the full url of the OxAPI to be called.
        """
        base_url: str = (
            oxapi.base_url if oxapi.base_url is not None else "https://api.oxolo.com"
        )  # TODO: remove hardcoding
        if verbose:
            oxapi.logger.info(base_url)
            oxapi.logger.info(self.api_version)
            oxapi.logger.info(self.type.value)
            oxapi.logger.info(self.model.value)
            oxapi.logger.info(self.version)

        return "/".join(
            [
                base_url,
                self.api_version,
                "model",  # TODO: remove hardcoding
                self.type.value,
                self.model.value,
                self.version,
                "inference",  # TODO: remove hardcoding
            ]
        )

    @classmethod
    def run(cls, *args, **kwargs):
        """Function to run and perform a call to any OxAPI model.

        Args:
            *args: any (see the derived class signature).
            **kwargs: any (see the derived class signature).

        Returns:
            ModelAPI : an object of ModelAPI class for fetching the result.
        """

        def __post_request(
            api: ModelAPI, body: dict, verbose: bool, raise_exceptions: bool
        ):
            """Performs a POST request on OxAPI endpoint and returns the
            result.

            Args:
                api: the ModelAPI object for performing the call.
                body: the body of the POST request
                verbose: optional, True to enable verbose mode.
                raise_exceptions: enables or disables the raising of exceptions in case of error. If False,
                you will be receiving only warnings.

            Returns:
                the result from the POST request.
            """
            if oxapi.api_key is None:
                raise InvalidAPIKeyException(
                    "API Key cannot be None: either you set it manually the value of oxapi.api_key, \
                or you set the OXAPI_KEY environment variable"
                )
            url: str = api.get_url(verbose=verbose)
            if verbose:
                oxapi.logger.info(url)
                oxapi.logger.info(body)
            res = requests.post(
                url,
                json=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": oxapi.api_key,
                },
            )
            api.parse_error_message(
                res, verbose=verbose, raise_exceptions=raise_exceptions
            )
            if api.error is not None:
                return None
            return res

        api: ModelAPI = kwargs.get("api")
        verbose: bool = kwargs.get("verbose")
        body: dict = kwargs.get("body")
        raise_exceptions: bool = kwargs.get("raise_exceptions")
        res = __post_request(
            api=api, body=body, verbose=verbose, raise_exceptions=raise_exceptions
        )
        return api, res

    def parse_error_message(
        self, api_response, verbose: bool = False, raise_exceptions: bool = True
    ):
        """Method to handle the error messages from the API.

        Args:
            api_response: the response received from the API.
            verbose: optional, True to enable verbose mode.
            raise_exceptions: default True, enables or disables the raising of exceptions in case of error. If False,
            you will be receiving only warnings.
        """
        if verbose:
            oxapi.logger.info("Response code: " + str(api_response.status_code))
        if api_response.status_code == 200:
            return
        elif api_response.status_code == 401:
            self.error = InvalidAPIKeyException(
                message=api_response.json()["message"],
                headers=api_response.headers,
                http_status=api_response.status_code,
                http_body=api_response.json(),
            )
        elif api_response.status_code == 403:
            self.error = NotAllowedException(
                message=api_response.json()["message"],
                headers=api_response.headers,
                http_status=api_response.status_code,
                http_body=api_response.json(),
            )
        elif api_response.status_code == 404:
            self.error = NotFoundException(
                message=api_response.json()["message"],
                headers=api_response.headers,
                http_status=api_response.status_code,
                http_body=api_response.json(),
            )
        else:
            self.error = OxAPIError(
                message=api_response.json()["message"],
                headers=api_response.headers,
                http_status=api_response.status_code,
                http_body=api_response.json(),
            )
        if self.error is not None:
            if not raise_exceptions:
                oxapi.logger.warning(
                    "Request failed: {0}, ERROR: {1}".format(
                        api_response.url, api_response.json()["message"]
                    )
                )
            else:
                raise self.error

    def set_params(self, **kwargs):
        """Function for setting attributes to the objects.

        Args:
            **kwargs: any parameters.
        """
        for key, value in kwargs.items():
            if key == "body":
                key = "_body"
            self.__setattr__(key, value)
