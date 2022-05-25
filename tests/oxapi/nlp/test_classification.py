import pytest

import oxapi
from oxapi.nlp.classification import Classification


def test_api_key():
    oxapi.api_key = None
    with pytest.raises(ValueError) as ve:
        Classification.create(model="ciro", texts=["esposito"])
