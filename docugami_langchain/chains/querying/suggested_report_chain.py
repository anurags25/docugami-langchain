from operator import itemgetter
from typing import AsyncIterator, List, Optional

from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableLambda

from docugami_langchain.base_runnable import BaseRunnable, TracedResponse
from docugami_langchain.chains.helpers import formatted_summaries
from docugami_langchain.output_parsers.line_separated_list import (
    LineSeparatedListOutputParser,
)
from docugami_langchain.params import RunnableParameters, RunnableSingleParameter


class SuggestedReportChain(BaseRunnable[list[str]]):
    def runnable(self) -> Runnable:
        """
        Custom runnable for this chain.
        """

        return {
            "summaries": itemgetter("summaries") | RunnableLambda(formatted_summaries),
        } | super().runnable()

    def params(self) -> RunnableParameters:
        return RunnableParameters(
            inputs=[
                RunnableSingleParameter(
                    "summaries",
                    "SUMMARIES",
                    "Summaries of representative documents from a set of documents",
                ),
            ],
            output=RunnableSingleParameter(
                "suggested_report_columns",
                "SUGGESTED REPORT COLUMNS",
                "Up to 20 suggested columns for an automatically generated report against documents similar to the ones provided.",
            ),
            task_description="suggests columns for an automatically generated report against a set of documents, given some summaries of representative documents from the set",
            additional_instructions=[
                "- Generate 'human-like' column labels, i.e. things a human familiar with this particular set of documents might want to know in a diagnostic report about this set of documents",
                "- Bias towards columns highly likely to be found in all or most of the documents.",
                "- Avoid columns that are highly likely to contain boilerplate or uninteresting information that is similar for all the documents.",
                "- Do not include Document Name or File Name in your list, since those are included automatically by the system.",
                "- Make sure the column names you generate are only alphanumeric, no special characters or parentheses.",
                "- Generate suggested columns as a list, one per line.",
            ],
            additional_runnables=[LineSeparatedListOutputParser()],
            stop_sequences=["\n\n", "<s>", "</s>", "|"],
            key_finding_output_parse=False,  # set to False for streaming
        )

    def run(  # type: ignore[override]
        self,
        summaries: List[Document],
        config: Optional[dict] = None,
    ) -> list[str]:
        if not summaries:
            raise Exception("Input required: summaries")

        return super().run(
            summaries=summaries,
            config=config,
        )

    def run_stream(  # type: ignore[override]
        self,
        summaries: List[Document],
        config: Optional[dict] = None,
    ) -> AsyncIterator[TracedResponse[list[str]]]:
        if not summaries:
            raise Exception("Input required: summaries")

        return super().run_stream(
            summaries=summaries,
            config=config,
        )

    def run_batch(  # type: ignore[override]
        self,
    ) -> list[list[str]]:
        raise NotImplementedError()
