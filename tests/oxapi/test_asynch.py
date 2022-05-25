import unittest.mock as mock

import pytest

import oxapi
from oxapi.asynch import AsyncCallPipe
from oxapi.nlp.encoding import Encoding
from oxapi.nlp.transformation import Transformation
from tests.testing_utils import MockedResponse


class TestAsyncCallPipe:
    """Tests for AsyncCallPipe class."""

    @pytest.fixture
    def mocked_answer(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        mocked_answer1 = MockedResponse(
            status_code=200, message={"results": [["Test!"]]}
        )
        mocked_answer2 = MockedResponse(
            status_code=200,
            message={"results": [[1.0, 1.1, 1.2, 1.3], [1.0, 1.1, 1.2, 1.3]]},
        )
        return [mocked_answer1, mocked_answer2]

    def test_empty_run(self):
        """Testing run function on empty call list."""
        asy = AsyncCallPipe()
        res = asy.run()
        assert res is None

    def test_run(self, mocked_answer):
        """Testing run function.

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"
        texts = ["test", "test again"]
        api1 = Encoding.prepare(model="mpnet-base-v2", texts=texts)
        api2 = Transformation.prepare(model="punctuation-imputation", texts=texts)
        asy = AsyncCallPipe([api1, api2])
        with mock.patch("oxapi.asynch.grequests.map", return_value=mocked_answer):
            res = asy.run()

            assert res[0].result is not None and res[1].result is not None

    def test_add_single(self, mocked_answer):
        """Testing add function (single add).

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"
        texts = ["test", "test again"]
        api1 = Encoding.prepare(model="mpnet-base-v2", texts=texts)
        api2 = Transformation.prepare(model="punctuation-imputation", texts=texts)
        asy = AsyncCallPipe()
        asy.add([api1, api2])
        with mock.patch("oxapi.asynch.grequests.map", return_value=mocked_answer):
            res = asy.run()

            assert res[0].result is not None and res[1].result is not None

    def test_add_multiple(self, mocked_answer):
        """Testing add function (multiple add).

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"
        texts = ["test", "test again"]
        api1 = Encoding.prepare(model="mpnet-base-v2", texts=texts)
        api2 = Transformation.prepare(model="punctuation-imputation", texts=texts)
        asy = AsyncCallPipe([api1])
        asy.add(api2)
        with mock.patch("oxapi.asynch.grequests.map", return_value=mocked_answer):
            res = asy.run()

            assert res[0].result is not None and res[1].result is not None

    def test_flush(self):
        """Testing flush function."""
        oxapi.api_key = "test"
        texts = ["test", "test again"]
        api1 = Encoding.prepare(model="mpnet-base-v2", texts=texts)
        api2 = Transformation.prepare(model="punctuation-imputation", texts=texts)
        asy = AsyncCallPipe([api1, api2])
        asy.flush()
        with mock.patch("oxapi.asynch.grequests.map", return_value=[]):
            res = asy.run()

            assert res is None
