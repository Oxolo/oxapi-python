from typing import List, Union

import numpy as np

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.utils import OxapiType


class Encoding(ModelAPI):
    """Class for creating OxAPI calls to Encoding models."""

    @classmethod
    def create(
        cls,
        model: str,
        texts: List[str],
        api_version: str = None,
        version: str = None,
        verbose: bool = False,
        mock_answer: bool = False,
        raise_exceptions: bool = True,
    ):
        """
        Function to create and perform a call to OxAPI Encoding model
        Args:
            model (str): model to be invoked by the Encoding API.
            texts (List[str]): the list of text passed to the Encoding model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            verbose (bool): optional, True to enable verbose mode
            mock_answer (bool): optional, True to have in return a mocked answer for testing purposes
            raise_exceptions (bool): defult True, set to False to disable the raising of exceptions in case of error -
                you will be receiving only warnings.

        Returns:
            Encoding : an object of Encoding class for fetching the result.

        """
        api_version = oxapi.api_version if api_version is None else api_version
        # TODO: hardcoding to be removed, we should implement "latest" logic
        version = version if version is not None else "v1"
        body = {"texts": texts}
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=model,
            api_version=api_version,
            version=version,
        )
        api, res = super().create(
            api=api, verbose=verbose, body=body, raise_exceptions=raise_exceptions
        )
        api.set_params(result=res.json() if res is not None else res, input_texts=texts)
        return api

    def format_result(
        self, result_format: str = "numpy"
    ) -> Union[np.ndarray, dict, None]:
        """
        Function for getting the result processed in the available formats.
        Args:
            result_format (str): default 'numpy', desired format for the output. Available formats are: ['numpy', 'dict'].

        Returns:
            Union[numpy.ndarray, dict, None] : the result in the desired format; None if no result is available.

        """
        try:
            self.input_texts
        except AttributeError:
            oxapi.logger.warning("Input texts are not defined")
            return None
        try:
            self.result
        except AttributeError:
            oxapi.logger.warning("Results are not available")
            return None
        if self.result is None:
            oxapi.logger.warning("Results are not available")
            return None
        if result_format == "numpy":
            return np.array([np.array(el) for el in self.result["results"]])
        elif result_format == "dict":
            return {
                i: {
                    "text": self.input_texts[i],
                    "embedding": np.array(self.result["results"][i]),
                }
                for i in range(0, len(self.input_texts))
            }
        else:
            raise ValueError(
                "{0} is not a valid format for the output.\
            Available formats: ['numpy', 'dict']".format(
                    result_format
                )
            )

    @classmethod
    def prepare(
        cls,
        model: str,
        texts: List[str],
        api_version: str = None,
        version: str = None,
        mock_answer: bool = False,
    ):
        """
        Function to create a call to OxAPI Encoding model without performing it. It will only set the parameters.
        An Encoding object instantiated by the prepare function can be used in an AsynchronousCallPipe.
        Args:
            model (str): model to be invoked by the Encoding API.
            texts (List[str]): the list of text passed to the Encoding model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            mock_answer (bool): optional, True to have in return a mocked answer for testing purposes

        Returns:
            Encoding : an object of Encoding class having the parameters set.

        """
        body = {"texts": texts}
        version = version if version is not None else "v1"
        api_version = oxapi.api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=model,
            api_version=api_version,
            version=version,
        )
        api.set_params(body=body, input_texts=texts)
        return api

    @classmethod
    def list_models(cls):
        """
        TBD: Function to list of models for Classification
        Returns:

        """
        # TODO: remove stub
        pass
