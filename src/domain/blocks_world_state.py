from typing import Generator, Set


class BlocksWorldState:
    def __init__(self, current_state: list[int], actions: dict[str, dict[str, list[int]]], name: str = 'root') -> None:
        if self.__is_valid_state(current_state) is False:
            raise ValueError('The current state is not valid.')

        self.current = current_state
        self.avaliable_actions = self.__filter_avaliable_actions(actions)
        self.identifier = name

    def successors(self, actions: dict[str, dict[str, list[int]]]) -> Generator[BlocksWorldState, None, None]:
        for name, action in self.avaliable_actions.items():
            new_state = self.__expand(name, action, actions)
            yield new_state
            
    def __expand(self, action_name: str, action: dict[str, list[int]], actions: dict[str, dict[str, list[int]]]) -> BlocksWorldState:
        transition_state = set(self.current).difference(set(action['pre']))
        new_state = self.__resolve_consistent_state(
            transition_state, set(action['post']))

        return BlocksWorldState(new_state, actions, action_name)

    def __filter_avaliable_actions(self, actions: dict[str, dict[str, list[int]]]) -> dict[str, dict[str, list[int]]]:
        hook: dict[str, dict[str, list[int]]] = {}

        for action_name, conditions in actions.items():
            if set(conditions['pre']).issubset(set(self.current)):
                hook[action_name] = conditions
        return hook

    def __resolve_consistent_state(self, transition_state: Set[int], post_state: Set[int]) -> list[int]:
        abs_T = {abs(fact) for fact in transition_state}
        abs_P = {abs(fact) for fact in post_state}
        related_facts = abs_T.intersection(abs_P)

        if not related_facts:
            return list(transition_state.union(post_state))

        for fact in related_facts:
            transition_state.discard(fact)
            transition_state.discard(-fact)
        return list(transition_state.union(post_state))

    def __is_valid_state(self, state: list[int]) -> bool:
        abs_facts = [abs(fact) for fact in state]
        return len(abs_facts) == len(set(abs_facts))

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BlocksWorldState):
            return self.current == other.current
        return self is other
