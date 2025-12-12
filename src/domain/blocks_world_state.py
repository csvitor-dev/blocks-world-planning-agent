from __future__ import annotations
from typing import Generator, Set


class BlocksWorldState:
    def __init__(
        self,
        current_state: Set[int],
        actions: dict[str, dict[str, Set[int]]],
        name: str = 'root',
        parent: BlocksWorldState | None = None,
        real_cost: int = 0,
    ) -> None:
        if self.__is_valid_state(current_state) is False:
            raise ValueError('The current state is not valid.')

        self.current = set(current_state)
        self.key = str(sorted(self.current))
        self.actions = actions
        self.identifier = name
        self.parent = parent
        self.g = real_cost
        self.h = 0
        self.f = self.g

    def successors(self, actions: dict[str, dict[str, Set[int]]]) -> Generator['BlocksWorldState', None, None]:
        for name, action in self.actions.items():
            if action['pre'].issubset(self.current):
                yield self.__expand(name, action, actions)

    def __expand(self, action_name: str, action: dict[str, Set[int]], actions: dict[str, dict[str, Set[int]]]) -> BlocksWorldState:
        transition_state = self.current - action['pre']
        new_state = self.__resolve_consistent_state(
            transition_state, action['post'])

        return BlocksWorldState(new_state, actions, action_name, parent=self, real_cost=self.g + 1)

    def __resolve_consistent_state(self, transition_state: Set[int], post_state: Set[int]) -> Set[int]:
        only_positive_facts = {fact for fact in post_state if fact > 0}
        return transition_state.union(only_positive_facts)

    def __is_valid_state(self, state: Set[int]) -> bool:
        return len(state) == len({abs(fact) for fact in state})

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BlocksWorldState) and self.key == other.key
    
    def __lt__(self, other: BlocksWorldState) -> bool:
        return self.g < other.g
    
    def __gt__(self, other: BlocksWorldState) -> bool:
        return self.g > other.g

    def __repr__(self) -> str:
        return f'State({self.current})'
