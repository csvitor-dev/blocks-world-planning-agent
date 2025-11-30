""" 
TRABALHO DE INTELIGÊNCIA ARTIFICIAL

Equipe:
    - Agnaldo Erick Maia de Oliveira (539650) [ES]
    - Francisco Rodrigo de Santiago Pinheiro (554394) [ES]
    - Vitor Costa de Sousa (536678) [ES]
"""

from src.parser.domain_mapper import DomainMapper
from src.domain.clausal_form import ClausalForm
from src.domain.blocks_world_state import BlocksWorldState
from lib.utils import cmd
from typing import Set

def app() -> None:
    instance_id = cmd.pluck_instance_from_cmd_args()
    
    instance = DomainMapper.get_instance(instance_id)
    expression = ClausalForm(instance)
    initial_state = BlocksWorldState(expression.get_states()['initial'], expression.get_actions())
    
    nodes = print_state_space(initial_state, expression.get_actions())
    print(f'\nTotal unique states: {len(nodes)}')

def print_state_space(
    root: BlocksWorldState,
    instance_actions: dict[str, dict[str, list[int]]],
    visited: Set[int]|None = None
) -> Set[int]:
    if visited is None:
        visited = set()
    state_id = hash(root)

    if state_id in visited or len(root.avaliable_actions) == 0:
        return visited
    visited.add(state_id)

    for action, state in root.successors(instance_actions):
        print(action, state.current, state.avaliable_actions)
        print_state_space(state, instance_actions, visited)
    return visited

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print('Errors:', e.args)
