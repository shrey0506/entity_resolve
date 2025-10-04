import networkx as nx
from typing import Any, Optional, Dict

class GraphBuilderAgent:
    """
    Agent for building and managing a directed entity relationship graph using NetworkX.
    """

    def __init__(self):
        """
        Initialize the GraphBuilderAgent with an empty directed graph.
        """
        self.graph = nx.DiGraph()

    def add_entity(self, entity_id: Any, name: str, ubo: Optional[str] = None) -> None:
        """
        Add an entity node to the graph.

        Args:
            entity_id (Any): Unique identifier for the entity.
            name (str): Name of the entity.
            ubo (Optional[str]): Ultimate Beneficial Owner, if any.
        """
        self.graph.add_node(entity_id, label=name, ubo=ubo)

    def add_relationship(self, src: Any, dst: Any, rel_type: str) -> None:
        """
        Add a directed relationship (edge) between two entities.

        Args:
            src (Any): Source entity ID.
            dst (Any): Destination entity ID.
            rel_type (str): Type of relationship.
        """
        self.graph.add_edge(src, dst, type=rel_type)

    def export_graph(self) -> Dict:
        """
        Export the graph in node-link format.

        Returns:
            Dict: Node-link data representing the graph.
        """
        return nx.node_link_data(self.graph)
