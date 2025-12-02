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
    visited = set([initial_state.key])

    while queue:
        state: BlocksWorldState = queue.popleft()
        G.add_node(state.key, label=state.key)

        for next_state in state.successors(planning.actions):
            G.add_node(next_state.key, label=next_state.key)
            G.add_edge(state.key, next_state.key, label=next_state.identifier)

            if next_state.key not in visited:
                visited.add(next_state.key)
                queue.append(next_state)
    return G


def plot_graph(G: nx.DiGraph[str], generate_image: bool = False) -> None:
    seed = random.randint(100, 100000)
    nx.nx_pydot.write_dot(G, f'./assets/output/graph-{seed}.dot')

    if generate_image is False:
        return
    os.execv('/usr/bin/dot', ['dot', '-Tpng',
                              f'./assets/output/graph-{seed}.dot', '-o', f'./assets/output/graph-{seed}.png'])
