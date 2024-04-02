import os
from typing import Any

import pytest
import torch
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel

from docugami_langchain.chains.types.common import DataTypes, DocugamiDataType
from docugami_langchain.chains.types.data_type_detection_chain import (
    DataTypeDetectionChain,
)
from tests.common import TEST_DATA_DIR, verify_traced_response

TEST_INPUT_TEXT_ITEMS = [
    "22nndd M@ RCH 2oo7",
    "Signed on 07-01-1982",
    "This agreement was signed between Foo and Bar on the 2nd day of September, of the year twenty thirteen.",
    "02-01-23",
]
TEST_PARSED_DATA_TYPE: DocugamiDataType = DocugamiDataType(type=DataTypes.DATETIME)


@pytest.fixture()
def local_data_type_detection_chain(
    local_mistral7b: BaseLanguageModel,
    huggingface_minilm: Embeddings,
) -> DataTypeDetectionChain:
    """
    Local chain to do data type detection.
    """
    chain = DataTypeDetectionChain(llm=local_mistral7b, embeddings=huggingface_minilm)
    chain.load_examples(
        TEST_DATA_DIR / "examples/test_data_type_detection_examples.yaml"
    )
    return chain


@pytest.fixture()
def fireworksai_data_type_detection_chain(
    fireworksai_mixtral: BaseLanguageModel,
    huggingface_minilm: Embeddings,
) -> DataTypeDetectionChain:
    """
    FireworksAI chain to do data type detection.
    """
    chain = DataTypeDetectionChain(
        llm=fireworksai_mixtral, embeddings=huggingface_minilm
    )
    chain.load_examples(
        TEST_DATA_DIR / "examples/test_data_type_detection_examples.yaml"
    )
    return chain


@pytest.fixture()
def openai_data_type_detection_chain(
    openai_gpt35: BaseLanguageModel,
    openai_ada: Embeddings,
) -> DataTypeDetectionChain:
    """
    OpenAI chain to do data type detection.
    """
    chain = DataTypeDetectionChain(llm=openai_gpt35, embeddings=openai_ada)
    chain.load_examples(
        TEST_DATA_DIR / "examples/test_data_type_detection_examples.yaml"
    )
    return chain


@pytest.mark.skipif(not torch.cuda.is_available(), reason="No GPU available, skipping")
@pytest.mark.skipif(
    torch.cuda.is_available()
    and torch.cuda.get_device_properties(0).total_memory / (1024 * 1024 * 1024) < 15,
    reason="Not enough GPU memory to load model, need a larger GPU e.g. a 16GB T4",
)
def test_local_data_type_detection(
    local_data_type_detection_chain: DataTypeDetectionChain,
) -> Any:
    response = local_data_type_detection_chain.run(TEST_INPUT_TEXT_ITEMS)
    verify_traced_response(response)
    assert TEST_PARSED_DATA_TYPE == response.value


@pytest.mark.skipif(
    "FIREWORKS_API_KEY" not in os.environ, reason="Fireworks API token not set"
)
def test_fireworksai_data_type_detection(
    fireworksai_data_type_detection_chain: DataTypeDetectionChain,
) -> Any:
    response = fireworksai_data_type_detection_chain.run(TEST_INPUT_TEXT_ITEMS)
    verify_traced_response(response)
    assert TEST_PARSED_DATA_TYPE == response.value


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ, reason="OpenAI API token not set"
)
def test_openai_data_type_detection(
    openai_data_type_detection_chain: DataTypeDetectionChain,
) -> Any:
    response = openai_data_type_detection_chain.run(TEST_INPUT_TEXT_ITEMS)
    verify_traced_response(response)
    assert TEST_PARSED_DATA_TYPE == response.value