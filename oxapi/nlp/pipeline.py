from typing import List, Union

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.error import ModelNotFoundException
from oxapi.utils import OxapiNLPPipelineModel, OxapiType


class Pipeline(ModelAPI):
    """Class for creating OxAPI calls to Pipeline models."""

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
        """Function to run and perform a call to OxAPI Pipeline model.

        Args:
            model (str): model to be invoked by the Pipeline API.
            texts (List[str]): the list of text passed to the Pipeline model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            verbose (bool): optional, True to enable verbose mode
            raise_exceptions (bool): default True, set to False to disable the raising of exceptions in case of error -
            you will be receiving only warnings.

        Returns:
            Pipeline : an object of Pipeline class for fetching the result.
        """
        Pipeline.__check_input_model(model)
        api_version = oxapi.default_api_version if api_version is None else api_version
        version = version if version is not None else oxapi.default_model_version
        body = {"texts": texts}
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPPipelineModel(model),
            api_version=api_version,
            version=version,
        )
        api, res = super().run(
            api=api, verbose=verbose, body=body, raise_exceptions=raise_exceptions
        )
        api.set_params(result=res.json() if res is not None else res, input_texts=texts)
        return api

    def format_result(self, result_format: str = "dict") -> Union[dict, None]:
        """Function for getting the result processed in the available formats.

        Args:
            result_format (str): default 'dict', desired format for the output. Available formats are: ['dict'].

        Returns:
            Union[dict, None] : the result in the desired format; None if no result is available.
        """
        try:
            self.input_texts
        except AttributeError:
            oxapi.logger.warning("Input texts are not defined")
            return None
        if self.result is None:
            oxapi.logger.warning("Results are not available")
            return None
        if result_format == "dict":
            return {
                i: self.result["results"][i] for i in range(0, len(self.input_texts))
            }
        else:
            raise ValueError(
                "{0} is not a valid format for the output.\
            Available formats: ['dict']".format(
                    result_format
                )
            )

    @classmethod
    def prepare(
        cls, model: str, texts: List[str], api_version: str = None, version: str = None
    ):
        """Function to run a call to OxAPI Pipeline model without performing
        it. It will only set the parameters. A `Pipeline` object instantiated
        by the prepare function can be used in an `AsyncCallPipe`.

        Args:
            model (str): model to be invoked by the Pipeline API.
            texts (List[str]): the list of text passed to the Pipeline model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.

        Returns:
            Pipeline : an object of Pipeline class having the parameters set.
        """
        Pipeline.__check_input_model(model)
        body = {"texts": texts}
        version = version if version is not None else oxapi.default_model_version
        api_version = oxapi.default_api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPPipelineModel(model),
            api_version=api_version,
            version=version,
        )
        api.set_params(body=body, input_texts=texts)
        return api

    @classmethod
    def list_models(cls) -> List[str]:
        """Function to list of models for Pipeline.

        Returns:
            list : the model name list.
        """
        return [o.value for o in OxapiNLPPipelineModel]

    @staticmethod
    def __check_input_model(model_string: str):
        """Internal function for checking if the input model name exists in
        OxAPI.

        Args:
            model_string: the input model name.
        """
        try:
            OxapiNLPPipelineModel(model_string)
        except ValueError:
            raise ModelNotFoundException(
                "'{0}' is not a valid model for OxAPI Pipeline. Available models are {1}".format(
                    model_string, str(Pipeline.list_models())
                )
            )
