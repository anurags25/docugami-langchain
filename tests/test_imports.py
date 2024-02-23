from docugami_langchain import __all__

EXPECTED_BASE = [
    "BaseRunnable",
    "TracedResponse",
    "RunnableParameters",
    "RunnableSingleParameter",
]

EXPECTED_AGENTS = [
    "ReWOOAgent",
]
EXPECTED_CHAINS = [
    "AnswerChain",
    "ElaborateChunkChain",
    "SummarizeChunkChain",
    "SummarizeDocumentChain",
    "DescribeDocumentSetChain",
    "DocugamiExplainedSQLQueryChain",
    "SQLFixupChain",
    "SQLQueryExplainerChain",
    "SQLResultChain",
    "SQLResultExplainerChain",
    "SuggestedQuestionsChain",
    "SuggestedReportChain",
    "SimpleRAGChain",
]

EXPECTED_DOCUMENT_LOADERS = [
    "DocugamiLoader",
]

EXPECTED_OUTPUT_PARSERS = [
    "KeyfindingOutputParser",
    "LineSeparatedListOutputParser",
    "SoftReActJsonSingleInputOutputParser",
    "SQLFindingOutputParser",
    "TimeSpan",
    "TimespanOutputParser",
]

EXPECTED_RETRIEVERS = ["SearchType", "FusedSummaryRetriever"]

EXPECTED_ALL = (
    EXPECTED_BASE
    + EXPECTED_CHAINS
    + EXPECTED_DOCUMENT_LOADERS
    + EXPECTED_OUTPUT_PARSERS
    + EXPECTED_RETRIEVERS
)


def test_all_imports() -> None:
    assert sorted(EXPECTED_ALL) == sorted(__all__)
