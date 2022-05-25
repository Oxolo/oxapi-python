import unittest.mock as mock

import pytest

import oxapi
from oxapi.error import ModelNotFoundException
from oxapi.nlp.pipeline import Pipeline
from tests.testing_utils import MockedResponse


class TestPipeline:
    """Testing Pipeline class."""

    @pytest.fixture
    def mocked_answer(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        return MockedResponse(
            status_code=200, message={"results": [{"stuff": "other stuff"}]}
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
            api = Pipeline.create(model="en-core-web-lg", texts=["esposito"])
            assert api.result is not None

    def test_prepare(self):
        """Testing prepare function.

        Returns:
        """
        oxapi.api_key = "test"
        api = Pipeline.prepare(model="en-core-web-lg", texts=["test"])
        assert isinstance(api, Pipeline) and api.result is None

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
            api = Pipeline.create(model="en-core-web-lg", texts=["esposito"])

        res = api.format_result()
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
            api = Pipeline.create(model="en-core-web-lg", texts=["esposito"])

        with pytest.raises(ValueError) as ve:
            res = api.format_result("dino")

    def test_list_models(self):
        """
        Testing list_model function
        Returns:

        """
        models = Pipeline.list_models()
        assert isinstance(Pipeline.list_models(), list) and len(models) > 0

    def test_wrong_model_input(self):
        """Testing exception raising when passed as input a non-existing model
        name.

        Returns:
        """
        with pytest.raises(ModelNotFoundException):
            api = Pipeline.create(model="best-pipeline-ever", texts=["text"])
