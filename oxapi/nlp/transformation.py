from typing import List, Union

import pandas as pd

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.error import ModelNotFoundException
from oxapi.utils import OxapiNLPTransformationModel, OxapiType


class Transformation(ModelAPI):
    """Class for creating OxAPI calls to Transformation models."""

    @classmethod
    def run(
        cls,
        model: str,
        texts: List[str],
        api_version: str = None,
        version: str = None,
        verbose: bool = False,
        raise_exceptions: bool = True,
    ):
        """Function to run and perform a call to OxAPI Transformation model.

        Args:
            model (str): model to be invoked by the Transformation API.
            texts (List[str]): the list of text passed to the Transformation model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            verbose (bool): optional, True to enable verbose mode
            raise_exceptions (bool): default True, set to False to disable the raising of exceptions in case of error -
            you will be receiving only warnings.

        Returns:
            Transformation : an object of Transformation class for fetching the result.
        """
        Transformation.__check_input_model(model)
        api_version = oxapi.default_api_version if api_version is None else api_version
        version = version if version is not None else oxapi.default_model_version
        body = {"texts": texts}
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPTransformationModel(model),
            api_version=api_version,
            version=version,
        )
        api, res = super().run(
            api=api, verbose=verbose, body=body, raise_exceptions=raise_exceptions
        )
        api.set_params(result=res.json() if res is not None else res, input_texts=texts)
        return api

    def format_result(
        self, result_format: str = "pd"
    ) -> Union[pd.DataFrame, dict, None]:
        """Function for getting the result processed in the available formats.

        Args:
            result_format (str): default 'pd', desired format for the output. Available formats are: ['pd', 'dict'].

        Returns:
            Union[pandas.Dataframe, dict, None] : the result in the desired format; None if no result is available.
        """
        try:
            self.input_texts
        except AttributeError:
            oxapi.logger.warning("Input texts are not defined")
            return None
        if self.result is None:
            oxapi.logger.warning("Results are not available")
            return None
        if result_format == "pd":
            tmp_in = pd.DataFrame(self.input_texts, columns=["text"])
            tmp_out = pd.DataFrame(self.result["results"], columns=["output"])
            return pd.concat([tmp_in, tmp_out], axis=1)
        elif result_format == "dict":
            return {
                i: {"text": self.input_texts[i], "output": self.result["results"][i]}
                for i in range(0, len(self.input_texts))
            }
        else:
            raise ValueError(
                "{0} is not a valid format for the output.\
            Available formats: ['pd', 'dict']".format(
                    result_format
                )
            )

    @classmethod
    def prepare(
        cls, model: str, texts: List[str], api_version: str = None, version: str = None
    ):
        """Function to run a call to OxAPI Transformation model without
        performing it. It will only set the parameters. A `Transformation`
        object instantiated by the prepare function can be used in an
        `AsyncCallPipe`.

        Args:
            model (str): model to be invoked by the Transformation API.
            texts (List[str]): the list of text passed to the Transformation model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.

        Returns:
            Transformation : an object of Transformation class having the parameters set.
        """
        Transformation.__check_input_model(model)
        body = {"texts": texts}
        version = version if version is not None else oxapi.default_model_version
        api_version = oxapi.default_api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPTransformationModel(model),
            api_version=api_version,
            version=version,
        )
        api.set_params(body=body, input_texts=texts)
        return api

    @classmethod
    def list_models(cls) -> List[str]:
        """Function to list of models for Transformation.

        Returns:
            list : the model name list.
        """
        return [o.value for o in OxapiNLPTransformationModel]

    @staticmethod
    def __check_input_model(model_string: str):
        """Internal function for checking if the input model name exists in
        OxAPI.

        Args:
            model_string: the input model name.
        """
        try:
            OxapiNLPTransformationModel(model_string)
        except ValueError:
            raise ModelNotFoundException(
                "'{0}' is not a valid model for OxAPI Transformation. Available models are {1}".format(
                    model_string, str(Transformation.list_models())
                )
            )
