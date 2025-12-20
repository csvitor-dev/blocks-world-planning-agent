from typing import Set

class StripsNotation:
    def __init__(self, instance_ref: str, actions: list[str], initial_state: str, goal_state: str) -> None:
        self.instance_ref = instance_ref
        self.__facts: Set[str] = set()
        self.__actions = self.__create_actions(actions)
        self.__initial_state = self.__split_facts(initial_state)
        self.__goal_state = self.__split_facts(goal_state)
        self.__atoms = self.__extract_atoms()
    
    @property
    def actions(self) -> dict[str, dict[str, list[str]]]:
        return self.__actions

    @property
    def states(self) -> dict[str, list[str]]:
        return {
            'initial': self.__initial_state,
            'goal': self.__goal_state,
        }
    
    @property
    def avaliable_facts(self) -> list[str]:
        return list(self.__facts)

    @property
    def atoms(self) -> list[str]:
        return list(self.__atoms)
    
    def __extract_atoms(self) -> Set[str]:
        hook: Set[str] = set()
        
        for fact in self.__initial_state:
            partitions = fact.split('_')
            
            if partitions[0] in ['clear', 'ontable']:
                hook.add(partitions[1])
            elif partitions[0] == 'on':
                hook.add(partitions[1])
                hook.add(partitions[2])
        return hook

    def __create_actions(self, raw_actions: list[str]) -> dict[str, dict[str, list[str]]]:
        hook: dict[str, dict[str, list[str]]] = {}

        for i in range(0, len(raw_actions), 3):
            preconditions, post_conditions = self.__split_facts(
                raw_actions[i+1]), self.__split_facts(raw_actions[i+2])
            self.__extract_facts_from(preconditions + post_conditions)

            hook[raw_actions[i]] = {
                'pre': preconditions,
                'post': post_conditions
            }
        return hook

    def __split_facts(self, raw_state: str) -> list[str]:
        return raw_state.split(';')

    def __extract_facts_from(self, facts: list[str]) -> None:
        for fact in facts:
            self.__facts.add(fact)
