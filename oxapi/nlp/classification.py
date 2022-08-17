from typing import List, Union

import pandas as pd

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.error import ModelNotFoundException
from oxapi.utils import OxapiNLPClassificationModel, OxapiType


class Classification(ModelAPI):
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
        """Function to run and perform a call to OxAPI Classification model.

        Args:
            model (str): model to be invoked by the Classification API.
            texts (List[str]): the list of text passed to the Classification model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.
            verbose (bool): optional, True to enable verbose mode
            raise_exceptions (bool): default True, set to False to disable the raising of exceptions in case of error -
            you will be receiving only warnings.

        Returns:
            Classification : an object of Classification class for fetching the result.
        """
        Classification.__check_input_model(model)
        body = {"texts": texts}
        version = version if version is not None else oxapi.default_model_version
        api_version = oxapi.default_api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPClassificationModel(model),
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

        labels = self.model.get_labels()
        if self.model == OxapiNLPClassificationModel.DIALOG_TOPICS:
            input_texts = ["\n".join(self.input_texts)]
        else:
            input_texts = self.input_texts

        if result_format == "pd":
            tmp_in = pd.DataFrame(input_texts, columns=["text"])
            tmp_out = pd.DataFrame(self.result["results"], columns=labels)
            return pd.concat([tmp_in, tmp_out], axis=1)
        elif result_format == "dict":

            if self.model == OxapiNLPClassificationModel.DIALOG_TOPICS:
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
                        tmp_out[k]["output"][labels[i]] = self.result["results"][k][i]

            return tmp_out
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
        """Function to run a call to OxAPI Classification model without
        performing it. It will only set the parameters. A `Classification`
        object instantiated by the prepare function can be used in an
        ``AsyncCallPipe``.

        Args:
            model (str): model to be invoked by the Classification API.
            texts (List[str]): the list of text passed to the Classification model.
            api_version (str): version of the API; if nothing is passed, default value will be used.
            version (str): version of the model; if nothing is passed, default value will be used.

        Returns:
            Classification : an object of Classification class having the parameters set.
        """
        Classification.__check_input_model(model)
        body = {"texts": texts}
        version = version if version is not None else oxapi.default_model_version
        api_version = oxapi.default_api_version if api_version is None else api_version
        api = cls(
            oxapi_type=OxapiType.NLP,
            model=OxapiNLPClassificationModel(model),
            api_version=api_version,
            version=version,
        )
        api.set_params(body=body, input_texts=texts)
        return api

    @classmethod
    def list_models(cls) -> List[str]:
        """Function to list of models for Classification.

        Returns:
            list : the model name list.
        """
        return [o.value for o in OxapiNLPClassificationModel]

    @staticmethod
    def __check_input_model(model_string: str):
        """
        Internal function for checking if the input model name exists in OxAPI.
        Args:
            model_string: the input model name.

        Returns:

        """
        try:
            OxapiNLPClassificationModel(model_string)
        except ValueError:
            raise ModelNotFoundException(
                "'{0}' is not a valid model for OxAPI Classification. Available models are {1}".format(
                    model_string, str(Classification.list_models())
                )
            )
