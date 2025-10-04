from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.agents.entity_resolution_agent import EntityResolutionAgent
from src.agents.traversal_agent import TraversalAgent
from src.agents.graph_builder_agent import GraphBuilderAgent
from src.agents.human_review_agent import HumanReviewAgent
from src.agents.tools.dnb_loader import load_dnb
from src.agents.tools.cmd_loader import load_cmd


def build_workflow() -> Any:
    """
    Build and compile the CIB entity resolution and graph-building workflow.

    Returns:
        Any: The compiled workflow object.
    """
    dnb_df = load_dnb()
    cmd_df = load_cmd()

    er_agent = EntityResolutionAgent(dnb_df, cmd_df)
    traversal = TraversalAgent(cmd_df)
    graph_agent = GraphBuilderAgent()
    human = HumanReviewAgent()

    workflow = StateGraph(dict)

    def resolve_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve entities using the EntityResolutionAgent.

        Args:
            state (Dict[str, Any]): The current workflow state.

        Returns:
            Dict[str, Any]: Updated state with resolved entities.
        """
        dnb, cmd = er_agent.resolve(state["name"], state["postal"])
        state["dnb"] = dnb
        state["cmd"] = cmd
        return state

    def traverse_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traverse the entity hierarchy to find parent and children.

        Args:
            state (Dict[str, Any]): The current workflow state.

        Returns:
            Dict[str, Any]: Updated state with parent and children entities.
        """
        if state["cmd"] is not None:
            parent = traversal.get_parent(state["cmd"]["entity_id"])
            children = traversal.get_children(state["cmd"]["entity_id"])
            state["parent"] = parent
            state["children"] = children
        return state

    def graph_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build and update the entity relationship graph.

        Args:
            state (Dict[str, Any]): The current workflow state.

        Returns:
            Dict[str, Any]: Updated state with the graph.
        """
        if state["cmd"] is not None:
            graph_agent.add_entity(
                state["cmd"]["entity_id"],
                state["cmd"]["name"],
                state["cmd"]["ubo"]
            )
            if state.get("parent") is not None:
                graph_agent.add_entity(
                    state["parent"]["entity_id"].iloc[0],
                    state["parent"]["name"].iloc[0]
                )
                graph_agent.add_relationship(
                    state["parent"]["entity_id"].iloc[0],
                    state["cmd"]["entity_id"],
                    "PARENT_OF"
                )
            for _, child in state.get("children", []).iterrows():
                graph_agent.add_entity(child["entity_id"], child["name"])
                graph_agent.add_relationship(
                    state["cmd"]["entity_id"],
                    child["entity_id"],
                    "HAS_SUBSIDIARY"
                )
            state["graph"] = graph_agent.export_graph()
        return state

    def human_node(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Present the graph for human review.

        Args:
            state (Dict[str, Any]): The current workflow state.

        Returns:
            Dict[str, Any]: State after human review.
        """
        human.review(state["graph"])
        return state

    workflow.add_node("resolve", resolve_node)
    workflow.add_node("traverse", traverse_node)
    workflow.add_node("graph", graph_node)
    workflow.add_node("human", human_node)

    workflow.set_entry_point("resolve")
    workflow.add_edge("resolve", "traverse")
    workflow.add_edge("traverse", "graph")
    workflow.add_edge("graph", "human")
    workflow.add_edge("human", END)

    return workflow.compile()
