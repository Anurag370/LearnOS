from langgraph.graph import END, START, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.agents.tutor.nodes import (
    generate_answer,
    load_student_context,
    retrieve_context,
    validate_grounding,
)
from app.ai.agents.tutor.state import TutorState, MAX_TUTOR_RETRIES

def route_after_validation(
    state: TutorState,
) -> str:
    if state.get("grounded", False):
        return "end"

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count >= MAX_TUTOR_RETRIES:
        return "end"

    return "retry"

async def prepare_retry(
    state: TutorState,
) -> dict:
    return {
        "retry_count": state.get(
            "retry_count",
            0,
        ) + 1,
    }


def build_tutor_graph(
    session: AsyncSession,
):
    async def load_context_node(
        state: TutorState,
    ):
        return await load_student_context(
            state,
            session,
        )

    async def retrieve_node(
        state: TutorState,
    ):
        return await retrieve_context(
            state,
            session,
        )

    graph = StateGraph(TutorState)

    graph.add_node(
        "load_student_context",
        load_context_node,
    )

    graph.add_node(
        "retrieve_context",
        retrieve_node,
    )

    graph.add_node(
        "generate_answer",
        generate_answer,
    )

    graph.add_node(
        "validate_grounding",
        validate_grounding,
    )

    graph.add_node(
        "prepare_retry",
        prepare_retry,
    )

    graph.add_edge(
        START,
        "load_student_context",
    )

    graph.add_edge(
        "load_student_context",
        "retrieve_context",
    )

    graph.add_edge(
        "retrieve_context",
        "generate_answer",
    )

    graph.add_edge(
        "generate_answer",
        "validate_grounding",
    )

    graph.add_conditional_edges(
        "validate_grounding",
        route_after_validation,
        {
            "end": END,
            "retry": "prepare_retry",
        },
    )

    graph.add_edge(
        "prepare_retry",
        "retrieve_context",
    )

    return graph.compile()