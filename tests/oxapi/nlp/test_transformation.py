import unittest.mock as mock

import pandas as pd
import pytest

import oxapi
from oxapi.error import ModelNotFoundException
from oxapi.nlp.transformation import Transformation
from tests.testing_utils import MockedResponse


class TestTransformation:
    """Testing Transformation class."""

    @pytest.fixture
    def mocked_answer(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        return MockedResponse(status_code=200, message={"results": [["Test!"]]})

    def test_create(self, mocked_answer):
        """
        Testing create function.
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Transformation.create(model="punctuation-imputation", texts=["test"])
            assert api.result is not None

    def test_prepare(self):
        """Testing prepare function.

        Returns:
        """
        oxapi.api_key = "test"
        api = Transformation.prepare(model="punctuation-imputation", texts=["test"])
        assert isinstance(api, Transformation) and api.result is None

    def test_format_result_pandas(self, mocked_answer):
        """
        Testing format_result function (pandas format)
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Transformation.create(model="punctuation-imputation", texts=["test"])

        res = api.format_result()
        assert isinstance(res, pd.DataFrame)

    def test_format_result_dict(self, mocked_answer):
        """
        Testing format_result function (dict format)
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Transformation.create(model="punctuation-imputation", texts=["test"])

        res = api.format_result("dict")
        assert isinstance(res, dict)

    def test_format_result_wrong_format(self, mocked_answer):
        """
        Testing format_result function (wrong format)
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Transformation.create(
                model="punctuation-imputation", texts=["esposito"]
            )

        with pytest.raises(ValueError) as ve:
            res = api.format_result("dino")

    def test_list_models(self):
        """
        Testing list_model function
        Returns:

        """
        models = Transformation.list_models()
        assert isinstance(Transformation.list_models(), list) and len(models) > 0

    def test_wrong_model_input(self):
        """Testing exception raising when passed as input a non-existing model
        name.

        Returns:
        """
        with pytest.raises(ModelNotFoundException):
            api = Transformation.create(
                model="best-transformation-model-ever", texts=["text"]
            )
