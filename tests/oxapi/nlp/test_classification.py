import unittest.mock as mock
from typing import List

import pandas as pd
import pytest

import oxapi
from oxapi.error import ModelNotFoundException
from oxapi.nlp.classification import Classification
from tests.testing_utils import MockedResponse


class TestClassification:
    """Tests for Classification class."""

    @pytest.fixture
    def mocked_answer(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        return MockedResponse(
            status_code=200, message={"results": [["mocked_label", 1.0]]}
        )

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
            api = Classification.create(
                model="dialog-content-filter", texts=["esposito"]
            )
            assert api.result is not None

    def test_prepare(self):
        """Testing prepare function.

        Returns:
        """
        oxapi.api_key = "test"
        api = Classification.prepare(model="dialog-tag", texts=["test"])
        assert isinstance(api, Classification) and api.result is None

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
            api = Classification.create(
                model="dialog-content-filter", texts=["esposito"]
            )

        res = api.format_result()
        assert isinstance(res, pd.DataFrame)

    def test_format_result_dict(self, mocked_answer):
        """
        Testing format_results function (dict format).
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Classification.create(
                model="dialog-content-filter", texts=["esposito"]
            )

        res = api.format_result("dict")
        assert isinstance(res, dict)

    def test_format_result_wrong_format(self, mocked_answer):
        """
        Testing format_results function (wrong format).
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Classification.create(
                model="dialog-content-filter", texts=["esposito"]
            )

        with pytest.raises(ValueError) as ve:
            res = api.format_result("dino")

    def test_list_models(self):
        """
        Testing list_model function
        Returns:

        """
        models = Classification.list_models()
        assert isinstance(Classification.list_models(), list) and len(models) > 0

    def test_wrong_model_input(self):
        """Testing exception raising when passed as input a non-existing model
        name.

        Returns:
        """
        with pytest.raises(ModelNotFoundException):
            api = Classification.create(
                model="best-classification-model-ever", texts=["text"]
            )
