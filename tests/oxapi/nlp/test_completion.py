import unittest.mock as mock

import pandas as pd
import pytest

import oxapi
from oxapi.error import ModelNotFoundException
from oxapi.nlp.completion import Completion
from tests.testing_utils import MockedResponse

from oxapi.utils import OxapiNLPCompletionModel, OxapiType


class TestCompletion:
    @pytest.fixture
    def mocked_answer(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        return MockedResponse(
            status_code=200, message={"results": ["I love writing tests."]}
        )

    def test_create(self, mocked_answer):
        """
        Testing create function.
        Args:
            mocked_answer: the mocked answer from grequests.

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Completion.create(
                model="gpt-neo-2-7b",
                prompt="I am a good programmer, therefore ",
            )
            assert api.result is not None

    def test_prepare(self):
        """Testin prepare function.

        """
        oxapi.api_key = "test"
        api = Completion.prepare(
            model="gpt-neo-2-7b", prompt="Nobody is such a good programmer"
        )
        assert isinstance(api, Completion) and api.result is None

    def test_format_result_pandas(self, mocked_answer):
        """
        Testing format_result function (pandas format)
        Args:
            mocked_answer: the mocked answer from grequests.

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Completion.create(
                model="gpt-neo-2-7b",
                prompt="I am a good programmer, therefore ",
            )

        res = api.format_result("pd")
        assert isinstance(res, pd.DataFrame)

    def test_format_result_str(self, mocked_answer):
        """
        Testing format_result function (string format)
        Args:
            mocked_answer: the mocked answer from grequests.

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Completion.create(
                model="gpt-neo-2-7b",
                prompt="I am a good programmer, therefore ",
            )

        res = api.format_result()
        assert isinstance(res, str)

    def test_format_result_wrong_format(self, mocked_answer):
        """
        Testing format_result function (wrong format)
        Args:
            mocked_answer: the mocked answer from grequests.

        """
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Completion.create(
                model="gpt-neo-2-7b",
                prompt="I am a good programmer, therefore ",
            )

        with pytest.raises(ValueError) as ve:
            res = api.format_result("dino")

    def test_list_models(self):
        """
        Testing list_model function

        """
        models = Completion.list_models()
        assert isinstance(Completion.list_models(), list) and len(models) > 0

    def test_wrong_model_input(self):
        """Testing exception raising when passed as input a non-existing model
        name.

        """
        with pytest.raises(ModelNotFoundException):
            api = Completion.create(model="best-completion-model-ever", prompt="text")

    def test_none_result(self):
        """
        Testing format_result function when result doesn't exist yet

        """
        oxapi.api_key = "test"
        api = Completion.prepare(model="gpt-neo-2-7b", prompt="test")
        assert api.format_result() is None

    def test_input_texts_not_defined(self):
        """
        Testing format_result function when input doesn't exist yet

        """
        oxapi.api_key = "test"
        api = Completion(
            model=OxapiNLPCompletionModel("gpt-neo-2-7b"),
            version="v1",
            api_version="v1",
            oxapi_type=OxapiType.NLP,
        )
        assert api.format_result() is None

    def test_verbose(self, mocked_answer):
        """
        Testing create function with verbose setting.
        Args:
            mocked_answer: the mocked answer from grequests.

        Returns:

        """
        oxapi.api_key = "test"
        with mock.patch(
                "oxapi.abstract.api.grequests.map", return_value=[mocked_answer]
        ):
            api = Completion.create(
                model="gpt-neo-2-7b",
                prompt="I am a good programmer, therefore ",
                verbose=True,
            )
            assert api.result is not None
