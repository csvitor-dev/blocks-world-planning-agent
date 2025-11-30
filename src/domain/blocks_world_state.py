from typing import Generator

class BlocksWorldState:
    def __init__(self, current_state: list[int], actions: dict[str, dict[str, list[int]]]) -> None:
        self.current = current_state
        self.avaliable_actions = self.__filter_avaliable_actions(actions)

    def expand(self, action: dict[str, list[int]], actions: dict[str, dict[str, list[int]]]) -> BlocksWorldState:
        new_state = set(self.current).difference(set(action['pre'])).union(action['post'])
        return BlocksWorldState(list(new_state), actions)

    def successors(self, actions: dict[str, dict[str, list[int]]]) -> Generator[tuple[str, BlocksWorldState], None, None]:
        for name, action in self.avaliable_actions.items():
            new_state = self.expand(action, actions)
            yield (name, new_state)

    def __filter_avaliable_actions(self, actions: dict[str, dict[str, list[int]]]) -> dict[str, dict[str, list[int]]]:
        hook: dict[str, dict[str, list[int]]] = {}
        for action_name, conditions in actions.items():
            if set(conditions['pre']).issubset(set(self.current)):
                hook[action_name] = conditions
        return hook
    
    def __hash__(self) -> int:
        return hash(self.current)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, BlocksWorldState):
            return self.current == other.current
        return self is other
    