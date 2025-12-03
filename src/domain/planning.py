from typing import Generator
from src.support.factories.algorithm_factory import AlgorithmFactory
from src.domain.contracts.local_search_algorithm import LocalSearchAlgorithm
from src.domain.contracts.planning_contract import PlanningContract
from src.domain.blocks_world_state import BlocksWorldState
from src.domain.strips_notation import StripsNotation


class Planning(PlanningContract):
    def __init__(self, strips: StripsNotation):
        self.__map = self.__map_clauses(strips)
        self.__actions = self.__resolve_actions(strips.actions)

        states = strips.states
        self.__initial_state = self.__resolve_facts(states['initial'])
        self.__goal_state = self.__resolve_facts(states['goal'])

        self.__state_space = BlocksWorldState(
            self.__initial_state, self.__actions)

        self.__planner: LocalSearchAlgorithm | None = None

    @property
    def current_state(self) -> BlocksWorldState:
        return self.__state_space

    @property
    def map(self) -> dict[str, int]:
        return self.__map

    @property
    def actions(self) -> dict[str, dict[str, list[int]]]:
        return self.__actions

    @property
    def states(self) -> dict[str, list[int]]:
        return {
            'initial': self.__initial_state,
            'goal': self.__goal_state,
        }

    def successors(self) -> Generator[BlocksWorldState, None, None]:
        return self.__state_space.successors(self.__actions)

    def set_algoritm(self, algorithm_key: str) -> None:
        self.__planner = AlgorithmFactory.make(algorithm_key, self)

    def execute(self) -> None:
        if self.__planner is None:
            raise AssertionError('The algorithm is not set')
        self.__planner.execute()

    def __map_clauses(self, strips: StripsNotation) -> dict[str, int]:
        action_hook: dict[str, int] = {}

        for fact in strips.avaliable_facts:
            if fact not in action_hook.keys():
                action_hook[fact] = abs(action_hook.get(f'~{fact}', len(
                    action_hook) + 1)) if fact.startswith('~') is False else -action_hook.get(
                        fact[1:], len(action_hook) + 1)
        return action_hook

    def __resolve_facts(self, target: list[str]) -> list[int]:
        return sorted([self.__map[fact] for fact in target])

    def __resolve_actions(self, actions: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[int]]]:
        hook: dict[str, dict[str, list[int]]] = {}

        for action, conditions in actions.items():
            hook[action] = {
                'pre': self.__resolve_facts(conditions['pre']),
                'post': self.__resolve_facts(conditions['post']),
            }
        return hook
