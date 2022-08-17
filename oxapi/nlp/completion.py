from typing import List, Union

import pandas as pd

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.error import ModelNotFoundException
from oxapi.utils import OxapiNLPCompletionModel, OxapiType


class Completion(ModelAPI):
    """Class for creating OxAPI calls to Completion models."""

    @classmethod
    def run(
        cls,
        model: str,
        prompt: str,
        api_version: str = None,
        version: str = None,
        verbose: bool = False,
        raise_exceptions: bool = True,
        **kwargs
    ):
        """Function to run and perform a call to OxAPI Completion model.

        Args:
            model (str): model to be invoked by the Completion API.
            prompt (str): the prompt to be passed to the Completion model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            verbose (bool): optional, True to enable verbose mode
            raise_exceptions (bool): deafult True, set to False to disable the raising of exceptions in case of error - \
                you will be receiving only warnings.
            **kwargs: additional parameters for the API call. See the OxAPI documentation: https://api.oxolo.com/documentation#parameters

        Returns:
            Completion : an object of Completion class for fetching the result.
        """
        Completion.__check_input_model(model)
        body = kwargs
        body["prompt"] = prompt
        version = version if version is not None else oxapi.default_model_version
        api_version = oxapi.default_api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPCompletionModel(model),
            api_version=api_version,
            version=version,
        )
        api, res = super().run(
            api=api, verbose=verbose, body=body, raise_exceptions=raise_exceptions
        )
        api.set_params(result=res.json() if res is not None else res, prompt=prompt)
        return api

    def format_result(
        self, result_format: str = "str"
    ) -> Union[str, pd.DataFrame, None]:
        """Function for getting the result processed in the available formats.

        Args:
            result_format (str): default 'str', desired format for the output. Available formats are: ['str', 'pd'].

        Returns:
            Union[str, pandas.DataFrame, None] : the result in the desired format; None if no result is available.
        """
        try:
            self.prompt
        except AttributeError:
            oxapi.logger.warning("Input texts are not defined")
            return None
        if self.result is None:
            oxapi.logger.warning("Results are not available")
            return None

        if result_format == "pd":
            tmp_in = pd.DataFrame([self.prompt], columns=["prompt"])
            tmp_out = pd.DataFrame(self.result["results"], columns=["output"])
            return pd.concat([tmp_in, tmp_out], axis=1)
        elif result_format == "str":
            return self.result["results"][0]
        else:
            raise ValueError(
                "{0} is not a valid format for the output.\
            Available formats: ['str', 'pd']".format(
                    result_format
                )
            )

    @classmethod
    def prepare(
        cls,
        model: str,
        prompt: str,
        api_version: str = None,
        version: str = None,
        **kwargs
    ):
        """Function to run a call to OxAPI Completion model without performing
        it. It will only set the parameters. A `Completion` object instantiated
        by the prepare function can be used in an `AsyncCallPipe`.

        Args:
            model (str): model to be invoked by the Completion API.
            prompt (str): the prompt to be passed to the Completion model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            **kwargs: additional parameters for the API call. See the OxAPI documentation: https://api.oxolo.com/documentation#parameters

        Returns:
            Completion : an object of Completion class having the parameters set.
        """
        Completion.__check_input_model(model)
        body = kwargs
        body["prompt"] = prompt
        version = version if version is not None else oxapi.default_model_version
        api_version = oxapi.default_api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPCompletionModel(model),
            api_version=api_version,
            version=version,
        )
        api.set_params(body=body, prompt=prompt)
        return api

    @classmethod
    def list_models(cls) -> List[str]:
        """Function to list of models for Classification.

        Returns:
            list : the model name list.
        """
        return [o.value for o in OxapiNLPCompletionModel]

    @staticmethod
    def __check_input_model(model_string: str):
        """Internal function for checking if the input model name exists in
        OxAPI.

        Args:
            model_string: the input model name.
        """
        try:
            OxapiNLPCompletionModel(model_string)
        except ValueError:
            raise ModelNotFoundException(
                "'{0}' is not a valid model for OxAPI Completion. Available models are {1}".format(
                    model_string, str(Completion.list_models())
                )
            )
