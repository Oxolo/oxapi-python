from unittest import mock

import pytest

import oxapi
from oxapi.abstract.api import ModelAPI
from oxapi.error import (
    InvalidAPIKeyException,
    NotAllowedException,
    NotFoundException,
    OxAPIError,
)
from oxapi.nlp.classification import Classification
from oxapi.utils import OxapiNLPClassificationModel, OxapiType
from tests.testing_utils import MockedResponse


class TestModelAPI:
    """Tests for ModelAPI class."""

    @pytest.fixture
    def mocked_answer_classification(self):
        """Creates mocked response for testing purposes.

        Returns:
            list : mocked answers
        """
        return MockedResponse(
            status_code=200, message={"results": [["mocked_label", 1.0]]}
        )

    @staticmethod
    def build_mocked_error(status_code):
        """
        Creates mocked error response for testing purposes.
        Args:
            status_code:

        Returns:
            MockedResponse : the mocked error response from grequests.

        """
        return MockedResponse(
            status_code=status_code, message={"message": "error_message"}
        )

    def test_instantiation(self):
        """Test error at abstract class instantiation."""
        with pytest.raises(NotImplementedError):
            api = ModelAPI(
                OxapiNLPClassificationModel("dialog-topics"), OxapiType.NLP, "w", "v"
            )

    def test_api_key(self):
        """Testing error raising with not defined API Key."""
        oxapi.api_key = None
        with pytest.raises(InvalidAPIKeyException) as ve:
            Classification.create(model="dialog-topics", texts=["esposito"])

    def test_set_params(self):
        api = Classification.prepare("dialog-tag", ["mammamiaitaliano"])
        api.set_params(param1=1, param2=2)
        assert api.param1 == 1 and api.param2 == 2

    def test_general_error(self):
        """Testing general OxAPIError exception raising."""
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map",
            return_value=[TestModelAPI.build_mocked_error(500)],
        ):
            with pytest.raises(OxAPIError):
                api = Classification.create(
                    model="dialog-tag",
                    texts=[],
                )

    def test_not_found_error(self):
        """Testing NotFoundException exception raising."""
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map",
            return_value=[TestModelAPI.build_mocked_error(404)],
        ):
            with pytest.raises(NotFoundException):
                api = Classification.create(
                    model="dialog-tag",
                    texts=[],
                )

    def test_not_allowed_error(self):
        """Testing NotAllowedException exception raising."""
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map",
            return_value=[TestModelAPI.build_mocked_error(403)],
        ):
            with pytest.raises(NotAllowedException):
                api = Classification.create(
                    model="dialog-tag",
                    texts=[],
                )

    def test_invalid_key_error(self):
        """Testing InvalidAPIKeyException exception raising."""
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map",
            return_value=[TestModelAPI.build_mocked_error(401)],
        ):
            with pytest.raises(InvalidAPIKeyException):
                api = Classification.create(
                    model="dialog-tag",
                    texts=[],
                )

    def test_general_error_to_str(self):
        """Testing general OxAPIError exception to string."""
        oxapi.api_key = "test"
        with mock.patch(
            "oxapi.abstract.api.grequests.map",
            return_value=[TestModelAPI.build_mocked_error(500)],
        ):
            try:
                api = Classification.create(
                    model="dialog-tag",
                    texts=[],
                )
            except OxAPIError as oe:
                assert isinstance(str(oe), str)

    def test_str(self, mocked_answer_classification):
        """Testing __str__ function.

        Args:
            mocked_answer: the mocked answer from grequests.
        """
        oxapi.api_key = "test"

        with mock.patch(
            "oxapi.abstract.api.grequests.map",
            return_value=[mocked_answer_classification],
        ):
            api = Classification.create(model="dialog-content-filter", texts=["dizio"])
            assert isinstance(str(api), str)
