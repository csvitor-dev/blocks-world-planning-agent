import networkx as nx
from collections import deque
import os
from src.domain.blocks_world_state import BlocksWorldState


def build_state_space(initial: BlocksWorldState, actions: dict[str, dict[str, list[int]]]) -> nx.DiGraph[str]:
    G: nx.DiGraph[str] = nx.DiGraph()
    queue = deque([initial])
    visited = set([initial.identifier])

    while queue:
        state: BlocksWorldState = queue.popleft()
        G.add_node(state.identifier, label=str(state.current))

        for action_name, next_state in state.successors(actions):
            next_id = next_state.identifier

            if G.has_edge(state.identifier, next_id) or G.has_edge(next_id, state.identifier):
                continue
            G.add_edge(state.identifier, next_id, label=action_name)

            if next_id in visited:
                continue
            visited.add(next_id)
            queue.append(next_state)
    return G


def plot_graph(G: nx.DiGraph[str], generate_image: bool = False) -> None:
    pos = nx.spring_layout(G, k=2, iterations=200, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=500)
    nx.draw_networkx_edges(G, pos, arrows=True)

    nx.draw_networkx_labels(G, pos, font_size=8)

    edge_labels = {(u, v): data["label"] for u, v, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    nx.nx_pydot.write_dot(G, "./assets/graph.dot")

    if generate_image:
        os.execv('/usr/bin/dot', ['dot', '-Tpng',
                 './assets/graph.dot', '-o', './assets/graph.png'])
