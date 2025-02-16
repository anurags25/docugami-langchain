import os
from datetime import datetime
from typing import Any

import pytest
import torch
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel

from docugami_langchain.chains.types.date_add_chain import DateAddChain
from tests.common import TEST_DATA_DIR, verify_traced_response

TEST_MESSY_START_DATE = "at around $ept3mb3r I5 in thee year 2Oo3"
TEST_MESSY_END_DATE_OR_DURATION = "on the fivth annivrsary"
TEST_ADDED_DATE: datetime = datetime(2008, 9, 15)


def init_chain(llm: BaseLanguageModel, embeddings: Embeddings) -> DateAddChain:
    chain = DateAddChain(llm=llm, embeddings=embeddings)
    chain.load_examples(TEST_DATA_DIR / "examples/test_date_add_examples.yaml")
    return chain


@pytest.mark.skipif(not torch.cuda.is_available(), reason="No GPU available, skipping")
@pytest.mark.skipif(
    torch.cuda.is_available()
    and torch.cuda.get_device_properties(0).total_memory / (1024 * 1024 * 1024) < 15,
    reason="Not enough GPU memory to load model, need a larger GPU e.g. a 16GB T4",
)
def test_local_date_add(
    local_mistral7b: BaseLanguageModel,
    huggingface_minilm: Embeddings,
) -> Any:
    chain = init_chain(local_mistral7b, huggingface_minilm)
    response = chain.run(TEST_MESSY_START_DATE, TEST_MESSY_END_DATE_OR_DURATION)
    verify_traced_response(response)
    assert TEST_ADDED_DATE == response.value


@pytest.mark.skipif(
    "FIREWORKS_API_KEY" not in os.environ, reason="Fireworks API token not set"
)
def test_fireworksai_date_add(
    fireworksai_mixtral: BaseLanguageModel,
    huggingface_minilm: Embeddings,
) -> Any:
    chain = init_chain(fireworksai_mixtral, huggingface_minilm)
    response = chain.run(TEST_MESSY_START_DATE, TEST_MESSY_END_DATE_OR_DURATION)
    verify_traced_response(response)
    assert TEST_ADDED_DATE == response.value


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ, reason="OpenAI API token not set"
)
def test_openai_gpt4_date_add(
    openai_gpt4: BaseLanguageModel,
    openai_ada: Embeddings,
) -> Any:
    chain = init_chain(openai_gpt4, openai_ada)
    response = chain.run(TEST_MESSY_START_DATE, TEST_MESSY_END_DATE_OR_DURATION)
    verify_traced_response(response)
    assert TEST_ADDED_DATE == response.value
