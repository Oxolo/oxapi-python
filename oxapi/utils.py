from enum import Enum
from typing import List


class OxapiType(Enum):
    NLP = "nlp"


class OxapiNLPClassificationModel(Enum):
    """Enum for OxAPI NLP classification models."""

    DIALOG_CONTENT_FILTER = "dialog-content-filter"
    DIALOG_TOPICS = "dialog-topics"
    DIALOG_EMOTIONS = "dialog-emotions"
    DIALOG_TAG = "dialog-tag"

    def get_labels(self) -> List[str]:
        """Defines the list of class labels.

        Returns:
            List[str] : the list of labels
        """
        if self.value in [self.DIALOG_CONTENT_FILTER.value, self.DIALOG_TAG.value]:
            return ["label", "confidence_score"]
        elif self.value == self.DIALOG_EMOTIONS.value:
            return [
                "original_label",
                "ekman_label",
                "group_label",
                "confidence_score",
            ]
        elif self.value == self.DIALOG_TOPICS.value:
            return ["label"]


class OxapiNLPCompletionModel(Enum):
    """Enum for OxAPI NLP completion models."""

    GPT_NEO_27B = "gpt-neo-2-7b"
    GPT_J_6B = "gpt-j-6b"


class OxapiNLPEncodingModel(Enum):
    """Enum for OxAPI NLP encoding models."""

    ALL_MPNET_BASE_V2 = "all-mpnet-base-v2"
    ALL_MINILM_L6_V2 = "all-minilm-l6-v2"


class OxapiNLPPipelineModel(Enum):
    """Enum for OxAPI NLP pipeline models."""

    EN_CORE_WEB_LG = "en-core-web-lg"


class OxapiNLPTransformationModel(Enum):
    """Enum for OxAPI NLP transformation models."""

    PUNCT_IMPUTATION = "punctuation-imputation"
