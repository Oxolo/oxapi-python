import unittest.mock as mock

import numpy as np
import pytest

import oxapi
from oxapi.error import ModelNotFoundException
from oxapi.nlp.encoding import Encoding
from tests.testing_utils import MockedResponse


class TestEncoding:
    """Tests for Encoding class."""

    @pytest.fixture
    def mocked_answer(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        return MockedResponse(
            status_code=200,
            message={"results": [[1.0, 1.1, 1.2, 1.3], [1.0, 1.1, 1.2, 1.3]]},
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
            api = Encoding.create(model="mpnet-base-v2", texts=["esposito"])
            assert api.result is not None

    def test_prepare(self):
        """Testing prepare function.

        Returns:
        """
        oxapi.api_key = "test"
        api = Encoding.prepare(model="mpnet-base-v2", texts=["test"])
        assert isinstance(api, Encoding) and api.result is None

    def test_format_result_numpy(self, mocked_answer):
        """
        Testing format_result function (numpy format).
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Encoding.create(model="mpnet-base-v2", texts=["esposito"])

        res = api.format_result()
        assert isinstance(res, np.ndarray)

    def test_format_result_dict(self, mocked_answer):
        """
        Testing format_result function (dict format).
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Encoding.create(model="mpnet-base-v2", texts=["esposito"])

        res = api.format_result("dict")
        assert isinstance(res, dict)

    def test_format_result_wrong_format(self, mocked_answer):
        """
        Testing format_result function (wrong format).
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Encoding.create(model="mpnet-base-v2", texts=["esposito"])

        with pytest.raises(ValueError) as ve:
            res = api.format_result("dino")

    def test_list_models(self):
        """
        Testing list_model function
        Returns:

        """
        models = Encoding.list_models()
        assert isinstance(Encoding.list_models(), list) and len(models) > 0

    def test_wrong_model_input(self):
        """Testing exception raising when passed as input a non-existing model
        name.

        Returns:
        """
        with pytest.raises(ModelNotFoundException):
            api = Encoding.create(model="best-encoding-model-ever", texts=["text"])