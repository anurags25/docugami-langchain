import os

import pytest
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from rerankers.models.ranker import BaseRanker

from docugami_langchain.chains import SimpleRAGChain
from docugami_langchain.chains.rag.standalone_question_chain import (
    StandaloneQuestionChain,
)
from tests.common import (
    TEST_DATA_DIR,
    build_test_fused_retriever,
    verify_traced_response,
)
from tests.testdata.docsets.docset_test_data import (
    DOCSET_TEST_DATA,
    DocsetTestData,
)


def init_simple_rag_chain(
    test_data: DocsetTestData,
    llm: BaseLanguageModel,
    embeddings: Embeddings,
    re_ranker: BaseRanker,
) -> SimpleRAGChain:
    retriever = build_test_fused_retriever(
        llm=llm,
        embeddings=embeddings,
        re_ranker=re_ranker,
        data_dir=TEST_DATA_DIR / "docsets" / test_data.name,
    )

    standalone_questions_chain = StandaloneQuestionChain(
        llm=llm,
        embeddings=embeddings,
    )
    standalone_questions_chain.load_examples(
        TEST_DATA_DIR / "examples/test_standalone_question_examples.yaml"
    )

    return SimpleRAGChain(
        llm=llm,
        embeddings=embeddings,
        retriever=retriever,
    )


@pytest.mark.parametrize("test_data", DOCSET_TEST_DATA)
@pytest.mark.skipif(
    "FIREWORKS_API_KEY" not in os.environ, reason="Fireworks API token not set"
)
def test_fireworksai_simple_rag(
    test_data: DocsetTestData,
    fireworksai_mixtral: BaseLanguageModel,
    huggingface_minilm: Embeddings,
    mxbai_re_rank: BaseRanker,
) -> None:

    fireworksai_mixtral_simple_rag_chain = init_simple_rag_chain(
        test_data=test_data,
        llm=fireworksai_mixtral,
        embeddings=huggingface_minilm,
        re_ranker=mxbai_re_rank,
    )

    for question in test_data.questions:
        if not question.requires_report and not question.chat_history:
            answer = fireworksai_mixtral_simple_rag_chain.run(
                question=question.question
            )
            verify_traced_response(answer, question.acceptable_answer_fragments)


@pytest.mark.parametrize("test_data", DOCSET_TEST_DATA)
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ, reason="OpenAI API token not set"
)
def test_openai_gpt4_simple_rag(
    test_data: DocsetTestData,
    openai_gpt4: BaseLanguageModel,
    openai_ada: Embeddings,
    openai_gpt4_re_rank: BaseRanker,
) -> None:
    openai_gpt4_simple_rag_chain = init_simple_rag_chain(
        test_data=test_data,
        llm=openai_gpt4,
        embeddings=openai_ada,
        re_ranker=openai_gpt4_re_rank,
    )

    for question in test_data.questions:
        if not question.requires_report and not question.chat_history:
            answer = openai_gpt4_simple_rag_chain.run(
                question=question.question,
            )
            verify_traced_response(answer, question.acceptable_answer_fragments)
