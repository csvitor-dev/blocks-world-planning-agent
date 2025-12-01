import networkx as nx
from collections import deque
import os
import random
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.planning import Planning


def build_state_space(planning: Planning) -> nx.DiGraph[str]:
    G: nx.DiGraph[str] = nx.DiGraph()
    initial_state = planning.current_state
    queue = deque([initial_state])
    visited = set([initial_state.identifier])

    while queue:
        state: BlocksWorldState = queue.popleft()
        G.add_node(state.identifier, label=str(state.current))

        for next_state in state.successors(planning.actions):
            next_id = next_state.identifier

            if G.has_edge(state.identifier, next_id) or G.has_edge(next_id, state.identifier):
                continue
            G.add_edge(state.identifier, next_id, label=next_id)

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
    
    seed = random.randint(100, 100000)
    nx.nx_pydot.write_dot(G, f'./assets/output/graph-{seed}.dot')

    if generate_image:
        os.execv('/usr/bin/dot', ['dot', '-Tpng',
                 f'./assets/output/graph-{seed}.dot', '-o', f'./assets/output/graph-{seed}.png'])
