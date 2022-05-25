from unittest import mock

import pytest

import oxapi
from oxapi.abstract.api import ListResourcesAPI, ModelAPI
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

    @staticmethod
    def build_mocked_error(status_code):
        """
        Creates mocked error response for testing purposes.
        Args:
            status_code:

        Returns:

        """
        return MockedResponse(
            status_code=status_code, message={"message": "error_message"}
        )

    def test_instantiation(self):
        """Test error at abstract class instantiation.

        Returns:
        """
        with pytest.raises(NotImplementedError):
            api = ModelAPI(
                OxapiNLPClassificationModel("dialog-topic"), OxapiType.NLP, "w", "v"
            )

    def test_api_key(self):
        """Testing error raising with not defined API Key.

        Returns:
        """
        oxapi.api_key = None
        with pytest.raises(InvalidAPIKeyException) as ve:
            Classification.create(model="dialog-topic", texts=["esposito"])

    def test_set_params(self):
        api = Classification.prepare("dialog-tag", ["mammamiaitaliano"])
        api.set_params(param1=1, param2=2)
        assert api.param1 == 1 and api.param2 == 2

    def test_general_error(self):
        """Testing general OxAPIError exception raising.

        Returns:
        """
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
        """Testing NotFoundException exception raising.

        Returns:
        """
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
        """Testing NotAllowedException exception raising.

        Returns:
        """
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
        """Testing InvalidAPIKeyException exception raising.

        Returns:
        """
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


class TestListResourcesAPI:
    """Test class for ListResourcesAPI class."""

    def test_instantiation(self):
        """Test error at abstract class instantiation.

        Returns:
        """
        with pytest.raises(NotImplementedError):
            api = ListResourcesAPI()
