import unittest.mock as mock

import pandas as pd
import pytest

import oxapi
from oxapi.error import ModelNotFoundException
from oxapi.nlp.classification import Classification
from oxapi.utils import OxapiNLPClassificationModel, OxapiType
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

    @pytest.fixture
    def mocked_answer_dialog_topic(self):
        """Creates mocked response for testing purposes, specifically for
        dialog-topics model.

        Returns:
            list : mocked answers
        """
        return MockedResponse(status_code=200, message={"results": ["mocked_label"]})

    @pytest.fixture
    def mocked_answer_dialog_emotions(self):
        """Creates mocked response for testing purposes, specifically for
        dialog-emotions model.

        Returns:
            list : mocked answers
        """
        return MockedResponse(
            status_code=200,
            message={
                "results": [["mocked_label", "mocked_label2", "mocked_label3", 1.0]]
            },
        )

    def test_create(self, mocked_answer):
        """Testing run function.

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"

        with mock.patch("oxapi.abstract.api.requests.post", return_value=mocked_answer):
            api = Classification.run(model="dialog-content-filter", texts=["esposito"])
            assert api.result is not None

    def test_prepare(self):
        """Testing prepare function."""
        oxapi.api_key = "test"
        api = Classification.prepare(model="dialog-tag", texts=["test"])
        assert isinstance(api, Classification) and api.result is None

    def test_format_result_pandas(self, mocked_answer):
        """
        Testing format_result function (pandas format)
        Args:
            mocked_answer: the mocked answer from grequests.

        """
        oxapi.api_key = "test"
        with mock.patch("oxapi.abstract.api.requests.post", return_value=mocked_answer):
            api = Classification.run(model="dialog-content-filter", texts=["esposito"])

        res = api.format_result()
        assert isinstance(res, pd.DataFrame)

    def test_format_result_dict(self, mocked_answer):
        """Testing format_results function (dict format).

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"
        with mock.patch("oxapi.abstract.api.requests.post", return_value=mocked_answer):
            api = Classification.run(model="dialog-content-filter", texts=["esposito"])

        res = api.format_result("dict")
        assert isinstance(res, dict)

    def test_format_result_wrong_format(self, mocked_answer):
        """Testing format_results function (wrong format).

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"
        with mock.patch("oxapi.abstract.api.requests.post", return_value=mocked_answer):
            api = Classification.run(model="dialog-content-filter", texts=["esposito"])

        with pytest.raises(ValueError) as ve:
            res = api.format_result("dino")

    def test_list_models(self):
        """Testing list_model function."""
        models = Classification.list_models()
        assert isinstance(Classification.list_models(), list) and len(models) > 0

    def test_wrong_model_input(self):
        """Testing exception raising when passed as input a non-existing model
        name."""
        with pytest.raises(ModelNotFoundException):
            api = Classification.run(
                model="best-classification-model-ever", texts=["text"]
            )

    def test_none_result(self):
        """Testing format_result function when result doesn't exist yet."""
        oxapi.api_key = "test"
        api = Classification.prepare(model="dialog-tag", texts=["test"])
        assert api.format_result() is None

    def test_input_texts_not_defined(self):
        """Testing format_result function when input doesn't exist yet."""
        oxapi.api_key = "test"
        api = Classification(
            model=OxapiNLPClassificationModel("dialog-tag"),
            version="v1",
            api_version="v1",
            oxapi_type=OxapiType.NLP,
        )
        assert api.format_result() is None

    def test_dialog_topic_model(self, mocked_answer_dialog_topic):
        """
        Testing dialog-topics specific result.
        Args:
            mocked_answer_dialog_topic:

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.requests.post",
            return_value=mocked_answer_dialog_topic,
        ):
            api = Classification.run(model="dialog-topics", texts=["esposito"])

        assert isinstance(api.format_result("dict"), dict)

    def test_dialog_emotions_model(self, mocked_answer_dialog_emotions):
        """
        Testing dialog-topics specific result.
        Args:
            mocked_answer_dialog_emotions:

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.requests.post",
            return_value=mocked_answer_dialog_emotions,
        ):
            api = Classification.run(model="dialog-emotions", texts=["esposito"])

        assert isinstance(api.format_result(), pd.DataFrame)
