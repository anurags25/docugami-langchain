import logging
import os
from pathlib import Path

import pytest
from langchain_community.cache import SQLiteCache
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.globals import set_llm_cache
from langchain_core.language_models import BaseLanguageModel
from langchain_fireworks.chat_models import ChatFireworks
from langchain_fireworks.llms import Fireworks
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rerankers import Reranker
from rerankers.models.ranker import BaseRanker

# Turn on caching
LOCAL_LLM_CACHE_DB_FILE = os.environ.get(
    "LOCAL_LLM_CACHE", "/tmp/docugami/.langchain.db"
)
os.makedirs(Path(LOCAL_LLM_CACHE_DB_FILE).parent, exist_ok=True)
set_llm_cache(SQLiteCache(database_path=LOCAL_LLM_CACHE_DB_FILE))

# Enable logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def is_core_tests_only_mode() -> bool:
    core_tests_env_var = os.environ.get("DOCUGAMI_ONLY_CORE_TESTS")
    if not core_tests_env_var:
        return False
    else:
        if isinstance(core_tests_env_var, bool):
            return core_tests_env_var
        else:
            return str(core_tests_env_var).lower() == "true"


# Model fixtures
@pytest.fixture()
def fireworksai_mistral_7b() -> BaseLanguageModel:
    """
    Mistral_7b model hosted on fireworksai.
    """
    return Fireworks(
        model="accounts/fireworks/models/mistral-7b",
        cache=True,
        temperature=0,
        max_tokens=2 * 1024,  # includes input and output tokens
        model_kwargs={
            "context_length_exceeded_behavior": "truncate",
        },
    )


@pytest.fixture()
def fireworksai_mixtral() -> BaseLanguageModel:
    """
    Mixtral8x7b model hosted on fireworksai.
    """
    return ChatFireworks(
        model="accounts/fireworks/models/mixtral-8x7b-instruct",
        streaming=True,
        cache=True,
        temperature=0,
        max_tokens=32 * 1024,  # includes input and output tokens
        model_kwargs={
            "context_length_exceeded_behavior": "truncate",
        },
    )


@pytest.fixture()
def fireworksai_dbrx() -> BaseLanguageModel:
    """
    DBRX model hosted on fireworksai.
    """
    return ChatFireworks(
        model="accounts/fireworks/models/dbrx-instruct",
        streaming=True,
        cache=True,
        temperature=0,
        max_tokens=32 * 1024,  # includes input and output tokens
        model_kwargs={
            "context_length_exceeded_behavior": "truncate",
        },
    )


@pytest.fixture()
def huggingface_minilm() -> Embeddings:
    """
    MiniLM-L6-v2 embeddings running locally using huggingface.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )


@pytest.fixture()
def mxbai_re_rank() -> BaseRanker:
    return Reranker("mixedbread-ai/mxbai-rerank-base-v1", verbose=0)


@pytest.fixture()
def openai_gpt4() -> BaseLanguageModel:
    """
    GPT 4 model by OpenAI.
    """
    return ChatOpenAI(
        model="gpt-4-turbo",
        streaming=True,
        cache=True,
        temperature=0,
        max_tokens=2 * 1024,  # only output tokens
    )


@pytest.fixture()
def openai_ada() -> Embeddings:
    """
    Ada embeddings by OpenAI.
    """
    return OpenAIEmbeddings(model="text-embedding-ada-002", client=None)


@pytest.fixture()
def openai_gpt4_re_rank() -> BaseRanker:
    return Reranker("rankgpt", api_key=os.environ.get("OPENAI_API_KEY"), verbose=0)
