from typing import Generator, Set


class BlocksWorldState:
    def __init__(self, current_state: list[int], actions: dict[str, dict[str, list[int]]], name: str = 'root') -> None:
        if self.__is_valid_state(current_state) is False:
            raise ValueError('The current state is not valid.')

        self.current = sorted(current_state)
        self.key = str(self.current)
        self.avaliable_actions = self.__filter_avaliable_actions(actions)
        self.identifier = name

    def successors(self, actions: dict[str, dict[str, list[int]]]) -> Generator[BlocksWorldState, None, None]:
        for name, action in self.avaliable_actions.items():
            new_state = self.__expand(name, action, actions)
            yield new_state

    def __expand(self, action_name: str, action: dict[str, list[int]], actions: dict[str, dict[str, list[int]]]) -> BlocksWorldState:
        transition_state = set(self.current) - set(action['pre'])
        new_state = self.__resolve_consistent_state(
            transition_state, set(action['post']))

        return BlocksWorldState(new_state, actions, action_name)

    def __filter_avaliable_actions(self, actions: dict[str, dict[str, list[int]]]) -> dict[str, dict[str, list[int]]]:
        return {
            name: condition for name, condition in actions.items()
            if set(condition['pre']).issubset(set(self.current))
        }

    def __resolve_consistent_state(self, transition_state: Set[int], post_state: Set[int]) -> list[int]:
        only_positive_facts = {fact for fact in post_state if fact > 0}
        return list(transition_state.union(only_positive_facts))

    def __is_valid_state(self, state: list[int]) -> bool:
        return len(state) == len({abs(fact) for fact in state})

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BlocksWorldState) and self.key == other.key

    def __repr__(self) -> str:
        return f'State({self.current})'
