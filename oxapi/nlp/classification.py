from typing import List, Union

import pandas as pd

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.utils import OxapiType


class Classification(ModelAPI):
    """Class for creating OxAPI calls to Transformation models."""

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
        Function to create and perform a call to OxAPI Classification model
        Args:
            model (str): model to be invoked by the Classification API.
            texts (List[str]): the list of text passed to the Classification model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            verbose (bool): optional, True to enable verbose mode
            mock_answer (bool): optional, True to have in return a mocked answer for testing purposes
            raise_exceptions (bool): defult True, set to False to disable the raising of exceptions in case of error - \
                you will be receiving only warnings.

        Returns:
            Classification : an object of Classification class for fetching the result.

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
        api, res = super().create(
            api=api, verbose=verbose, body=body, raise_exceptions=raise_exceptions
        )
        api.set_params(result=res.json() if res is not None else res, input_texts=texts)
        return api

    def format_result(
        self, result_format: str = "pandas"
    ) -> Union[pd.DataFrame, dict, None]:
        """
        Function for getting the result processed in the available formats.
        Args:
            result_format (str): default 'pandas', desired format for the output. Available formats are: ['pandas', 'dict'].

        Returns:
            Union[pandas.Dataframe, dict, None] : the result in the desired format; None if no result is available.

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
        if result_format == "pandas":

            if self.model in ["dialog-content-filter", "dialog-tag"]:
                columns = ["label", "confidence_score"]
                input_texts = self.input_texts
            elif self.model == "dialog-emotions":
                columns = [
                    "original_label",
                    "ekman_label",
                    "group_label",
                    "confidence_score",
                ]
                input_texts = self.input_texts
            elif self.model == "dialog-topic":
                columns = ["label"]
                input_texts = ["\n".join(self.input_texts)]
            else:
                columns = ["label"]
                input_texts = self.input_texts
            tmp_in = pd.DataFrame(input_texts, columns=["text"])
            tmp_out = pd.DataFrame(self.result["results"], columns=columns)
            return pd.concat([tmp_in, tmp_out], axis=1)
        elif result_format == "dict":
            if self.model in ["dialog-content-filter", "dialog-tag"]:
                keys = ["label", "confidence_score"]
                input_texts = self.input_texts
            elif self.model == "dialog-emotions":
                keys = [
                    "original_label",
                    "ekman_label",
                    "group_label",
                    "confidence_score",
                ]
                input_texts = self.input_texts
            elif self.model == "dialog-topic":
                keys = ["label"]
                input_texts = ["\n".join(self.input_texts)]
            else:
                keys = ["label"]
                input_texts = self.input_texts

            if self.model == "dialog-topic":
                tmp_out = {
                    i: {
                        "text": input_texts[0],
                        "output": {"label": self.result["results"][0]},
                    }
                    for i in range(0, len(input_texts))
                }
            else:
                tmp_out = {
                    i: {"text": input_texts[i], "output": {}}
                    for i in range(0, len(input_texts))
                }
                for k in tmp_out.keys():
                    for i in range(0, len(self.result["results"][k])):
                        tmp_out[k]["output"][keys[i]] = self.result["results"][k][i]

            return tmp_out
        else:
            raise ValueError(
                "{0} is not a valid format for the output.\
            Available formats: ['pandas', 'dict']".format(
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
        Function to create a call to OxAPI Classification model without performing it. It will only set the parameters.
        A Classification object instantiated by the prepare function can be used in an AsynchronousCallPipe.
        Args:
            model (str): model to be invoked by the Classification API.
            texts (List[str]): the list of text passed to the Classification model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            mock_answer (bool): optional, True to have in return a mocked answer for testing purposes

        Returns:
            Classification : an object of Classification class having the parameters set.

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
